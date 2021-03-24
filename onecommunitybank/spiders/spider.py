import scrapy

from scrapy.loader import ItemLoader

from ..items import OnecommunitybankItem
from itemloaders.processors import TakeFirst

base = 'https://www.onecommunity.bank/category/news/page/{}/'

class OnecommunitybankSpider(scrapy.Spider):
	name = 'onecommunitybank'
	page = 1
	start_urls = [base.format(page)]

	def parse(self, response):
		post_links = response.xpath('//a[@class="btn"]/@href').getall()
		yield from response.follow_all(post_links, self.parse_post)

		if post_links:
			self.page += 1
			yield response.follow(base.format(self.page), self.parse)

	def parse_post(self, response):
		title = response.xpath('//h1/text()').get()
		description = response.xpath('//div[@class="post-body tight-text-flex-container"]//text()[normalize-space()]').getall()
		description = [p.strip() for p in description]
		description = ' '.join(description).strip()
		date = response.xpath('//div[@class="post-date"]/text()').get()

		item = ItemLoader(item=OnecommunitybankItem(), response=response)
		item.default_output_processor = TakeFirst()
		item.add_value('title', title)
		item.add_value('description', description)
		item.add_value('date', date)

		return item.load_item()
