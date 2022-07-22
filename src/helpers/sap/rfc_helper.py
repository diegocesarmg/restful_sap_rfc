from pyrfc import Connection


class RFCHelper:
    MAX_OR_CLAUSE = 1

    def __init__(self, user, passwd, ashost, sysnr, client, saprouter):
        self.conn = Connection(user=user, passwd=passwd, ashost=ashost,
                               sysnr=sysnr, client=client, saprouter=saprouter, lang="PT")

    def rfc_execute(self, rfc_name, params):
        rfc_result = self.conn.call(rfc_name, **params)
        # rfc_result = self.conn.call(rfc_name,
        #                             IS_ORDER_HEADER=params["IS_ORDER_HEADER"],
        #                             IS_ORDER_HEADER_X=params["IS_ORDER_HEADER_X"],
        #                             IT_ORDER_PARTNERS=params["IT_ORDER_PARTNERS"],
        #                             IT_ORDER_ITEMS=params["IT_ORDER_ITEMS"],
        #                             IT_ORDER_ITEMS_X=params["IT_ORDER_ITEMS_X"],
        #                             IT_ORDER_SCHEDULE_LINES=params["IT_ORDER_SCHEDULE_LINES"],
        #                             IT_ORDER_SCHEDULE_LINES_X=params["IT_ORDER_SCHEDULE_LINES_X"]
        #                             )

        result = {
            rfc_name: rfc_result
        }

        return result

    def convert_abap_number(self, s):
        ret = s.strip()

        # Tratamento para números negativos
        if ("-" in ret):
            ret = "-" + ret.replace("-", "")

        return float(ret)
