from lxml import etree as ET

xpath_all = ".//record"
xpath_failed = (
    ".//record["
    "./row/policy_evaluated/disposition != 'none' or "
    "./row/policy_evaluated/spf != 'pass' or "
    "./row/policy_evaluated/dkim != 'pass' or "
    "./auth_results/dkim/result != 'pass' or "
    "./auth_results/spf/result!='pass'"
    "]"
)


class DMARCRuaParser:
    def __init__(self, dns):
        self.dns = dns

    def parse(self, rua_report, include_all=False):
        root = ET.parse(rua_report)
        records = root.xpath(xpath_all if include_all else xpath_failed)
        data = []
        for record in records:
            row = self._parse_row(record)

            payload_from = self._get_payload_from(record)

            auth_results = self._parse_auth_results(record)

            data.append(
                [
                    row["source_ip"],
                    row["source_host"],
                    payload_from,
                    auth_results["envelop_from"],
                    row["dmarc_policy_evaluation"]["dmarc_disposition"],
                    row["dmarc_policy_evaluation"]["dkim_align"],
                    auth_results["dkim_auth"],
                    row["dmarc_policy_evaluation"]["spf_align"],
                    auth_results["spf_auth"],
                    row["count"],
                ]
            )
        return data

    def _parse_row(self, record):
        result = {}

        row = record.xpath("./row")[0]
        result["count"] = int(row.xpath("./count/text()")[0])
        source_ip = row.xpath("./source_ip/text()")[0]
        result["source_host"] = self.dns.reverse_name(source_ip)
        result["source_ip"] = source_ip
        policy_evaluated = row.xpath('./policy_evaluated')[0]
        result["dmarc_policy_evaluation"] = self._parse_dmarc_policy_evaluation(policy_evaluated)

        return result

    def _parse_dmarc_policy_evaluation(self, policy_evalution):
        result = {}

        result["dmarc_disposition"] = policy_evalution.xpath("./disposition/text()")[0]
        result["dkim_align"] = policy_evalution.xpath("./dkim/text()")[0]
        result["spf_align"] = policy_evalution.xpath("./spf/text()")[0]

        return result

    def _get_payload_from(self, record):
        identifiers = record.xpath('./identifiers')[0]
        header_from = identifiers.xpath('./header_from')[0]
        return header_from.text

    def _parse_auth_results(self, record):
        results = {}

        auth_results = record.xpath('./auth_results')[0]
        results["dkim_auth"] = next(
            filter(
                lambda result: result != "pass",
                map(
                    lambda result: result.text, auth_results.xpath("./dkim/result")
                ),
            ),
            "pass",
        )
        results["spf_auth"] = next(
            filter(
                lambda result: result != "pass",
                map(lambda result: result.text, auth_results.xpath("./spf/result")),
            ),
            "pass",
        )

        results["envelop_from"] = next(
            filter(
                lambda result: result,
                map(lambda result: result.text, auth_results.xpath("./spf/domain")),
            ),
            "",
        )

        return results
