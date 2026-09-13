from datetime import datetime, timedelta
from parser.items import CurrencyRateItem

import scrapy
from scrapy import Selector, Spider

URL_TEMPLATE = (
    "http://www.cbr.ru/scripts/XML_daily.asp"
    "?date_req={day}/{month}/{year}"
)


class CbrSpider(Spider):
    name = "cbr"

    async def start(self):
        today = datetime.now().date()

        for days_ago in range(10):
            target_date = today - timedelta(days=days_ago)

            url = URL_TEMPLATE.format(
                day=f"{target_date.day:02d}",
                month=f"{target_date.month:02d}",
                year=target_date.year,
            )

            yield scrapy.Request(
                url=url,
                callback=self.parse,
            )

    def parse(self, response):
        selector = Selector(
            text=response.text,
            type="xml",
        )

        rate_date_raw = selector.xpath("/ValCurs/@Date").get()

        if rate_date_raw is None:
            return

        rate_date = datetime.strptime(
            rate_date_raw,
            "%d.%m.%Y",
        ).date()

        for valute in selector.xpath("//Valute"):
            yield CurrencyRateItem(
                code=valute.xpath("CharCode/text()").get(),
                name=valute.xpath("Name/text()").get(),
                nominal=int(
                    valute.xpath("Nominal/text()").get()
                ),
                value=float(
                    valute.xpath("Value/text()")
                    .get()
                    .replace(",", ".")
                ),
                date=rate_date,
            )
