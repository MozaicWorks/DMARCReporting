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
            row = record[0]
            source_ip = row[0].text
            count = int(row[1].text)

            source_host = self.dns.reverse_name(source_ip)

            dmarc_policy_evalution = row[2]
            dmarc_disposition = dmarc_policy_evalution[0].text
            dkim_align = dmarc_policy_evalution[1].text
            spf_align = dmarc_policy_evalution[2].text

            auth_results = record[2]
            dkim_auth = next(
                filter(
                    lambda result: result != "pass",
                    map(
                        lambda result: result.text, auth_results.xpath("./dkim/result")
                    ),
                ),
                "pass",
            )
            spf_auth = next(
                filter(
                    lambda result: result != "pass",
                    map(lambda result: result.text, auth_results.xpath("./spf/result")),
                ),
                "pass",
            )

            identifiers = record[1]
            payload_from = identifiers[0].text
            envelop_from = next(
                filter(
                    lambda result: result,
                    map(lambda result: result.text, auth_results.xpath("./spf/domain")),
                ),
                "",
            )

            data.append(
                [
                    source_ip,
                    source_host,
                    payload_from,
                    envelop_from,
                    dmarc_disposition,
                    dkim_align,
                    dkim_auth,
                    spf_align,
                    spf_auth,
                    count,
                ]
            )
        return data
