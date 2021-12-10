
from lxml import etree as ET


class DMARCRuaParser():
    def execute(self, rua_report):
        root = ET.parse(rua_report)
        records = root.xpath(
            (
                ".//record["
                "./row/policy_evaluated/disposition != 'none' or "
                "./row/policy_evaluated/spf!='pass' or "
                "./row/policy_evaluated/dkim!='pass'"
                "]"
            )
        )
        data = []
        for record in records:
            row = record[0]
            source_ip = row[0].text
            dmarc_policy_evalution = row[2]
            dmarc_disposition = dmarc_policy_evalution[0].text
            dkim_align = dmarc_policy_evalution[1].text
            spf_align = dmarc_policy_evalution[2].text

            data.append([source_ip, dmarc_disposition, dkim_align, spf_align])
        return data
