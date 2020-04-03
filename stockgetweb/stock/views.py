import pandas as pd

from datetime import datetime, timedelta

from django.shortcuts import render
from django.views.generic import TemplateView

from stockgetweb.crawl.tasks import my_name
# Create your views here.

###############################################################################
class StockFilterView(TemplateView):

    template_name = 'stock/stockFilter.html'

    def get_context_data(self, **kwargs):

        context = super(StockFilterView, self).get_context_data(**kwargs)

        time = datetime.now() + timedelta(seconds=10)

        my_name.apply_async(['test', ], eta=time)

        df = pd.read_csv('stockgetweb/crawl/test.csv')
        context.update({'stockData': df.to_html()})

        return context
###############################################################################
