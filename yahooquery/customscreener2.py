from yahooquery.screener import Screener
from yahooquery.utils.screeners import SCREENERS


turkish_stocks = {
    "desc": "Stocks listed on the Istanbul exchange",
    "id": "d29914e5-962d-46e9-9306-1d0620903b2e",
    "title": "Turkish stocks"
    }

SCREENERS['turkish_stocks'] = turkish_stocks


class CustomScreener(Screener):
    def __init__(self, **kwargs):
        super(CustomScreener, self).__init__(**kwargs)
        SCREENERS
    
    _CONFIG = Screener._CONFIG
    _CONFIG['customscreener'] = {
        "path": "https://query2.finance.yahoo.com/v1/finance/screener/saved",
        "response_field": "finance",
        "query": {
            "formatted": {"required": False, "default": False},
            "scrIds": {"required": True, "default": None},
            "count": {"required": False, "default": 25},
            },
        }
    
    def _construct_params(self, config, params):
        new_params = {}
        optional_params = [
            k
            for k in config["query"]
            if not config["query"][k]["required"]
            and config["query"][k]["default"] is not None
        ]
        for optional in optional_params:
            new_params.update(
                {optional: params.get(optional, config["query"][optional]["default"])}
            )
        new_params.update(self.default_query_params)
        new_params = {
            k: str(v).lower() if v is True or v is False else v
            for k, v in new_params.items()
        }
        return [dict(new_params, userId=self.userId, scrIds=scrId) for scrId in params["scrIds"]]


    def get_customscreeners(self, screen_ids, count=25):
        """Return list of predefined screeners from Yahoo Finance

        Parameters:
        screen_ids (str or list): Keys corresponding to list
            screen_ids = 'most_actives day_gainers'
            screen_ids = ['most_actives', 'day_gainers']
        count (int): Number of items to return, default=25
        """
        screen_ids = self._check_screen_ids(screen_ids)
        scrIds = [SCREENERS[screener]["id"] for screener in screen_ids]
        return self._get_data("customscreener", params={"scrIds": scrIds, "count": count, "userId": self.userId})
