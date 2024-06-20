from datetime import datetime
import re
import requests


class SalesrenderFacade:
    def __init__(self, api_token: str, api_link: str, company_id: int):
        self.api_url = f"{api_link}{company_id}/CRM"
        self.headers = {"Authorization": api_token}

    def _send_query(self, body: str) -> dict:
        response = requests.post(url=self.api_url, headers=self.headers, json={"query": body})
        return response.json()

    def update_status(self, order_id, status_id):
        body = """ 
        mutation   
          {{
            orderMutation {{
              updateOrder(
                input: {{
                  id : {order_id},
                  statusId: {status_id}
              }})
                {{
                id
                status {{
                      id
                }}
                data {{
                  stringFields {{
                      field {{
                          name
                      }}
                          value
                  }}
              }}
              }}
            }}
          }}
        """.format(order_id=order_id, status_id=status_id)
        return self._send_query(body)

    @staticmethod
    def get_body_for_updating_delivery_status(order_id, status_cs):
        current_time = datetime.now().strftime('%d.%m.%Y %H:%M:%S')
        return """
        orderMutation {{
            updateOrder(
              input: {{
                id : {order_id},
                orderData: {{
                  stringFields:
                    [
                      {{field: "DeliveryStatus", value: "{status_cs}" }},
                      {{field: "error_export", value: "OK" }},
                    ],
                  dateTimeFields: [
                    {{field: "date_of_status_cs", value: "{current_time}" }}
                  ]
                }}
            }})
              {{
              id
              status {{
                    id
              }}
              data {{
                stringFields {{
                    field {{
                        name
                    }}
                        value
                }}
            }}
            }}
          }}
        """.format(order_id=order_id, status_cs=status_cs, current_time=current_time)
    
    @staticmethod
    def get_body_for_updating_export_error(order_id, status_cs):
        current_time = datetime.now().strftime('%d.%m.%Y %H:%M:%S')
        return """
        orderMutation {{
            updateOrder(
              input: {{
                id : {order_id},
                orderData: {{
                  stringFields:
                    [
                      {{field: "error_export", value: "{status_cs}" }},
                    ],
                  dateTimeFields: [
                    {{field: "date_of_status_cs", value: "{current_time}" }}
                  ]
                }}
            }})
              {{
              id
              status {{
                    id
              }}
              data {{
                stringFields {{
                    field {{
                        name
                    }}
                        value
                }}
            }}
            }}
          }}
        """.format(order_id=order_id, status_cs=status_cs, current_time=current_time)    

    @staticmethod
    def get_order_id_by_order_number(order_tracker: str) -> str:
        return re.sub('\D', '', order_tracker)

    def update_status_cs(self, order_id, status_cs):
        body = f""" 
        mutation {{
            {self.get_body_for_updating_export_error(order_id, status_cs)}
        }}
        """
        return self._send_query(body)

    def update_several_statuses_cs(self, orders: dict):
        order_requests = []
        for i, (order_number, status) in enumerate(orders.items()):
            order_requests.append(
                f"orderMutation{i}: {self.get_body_for_updating_delivery_status(self.get_order_id_by_order_number(order_number), status)}"
            )
        body = """ 
            mutation {{
                {orders}
            }}
        """.format(orders="\n".join(order_requests))
        return self._send_query(body)
