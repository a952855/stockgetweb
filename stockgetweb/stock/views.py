import pandas as pd

from django.shortcuts import render
from django.views.generic import TemplateView

# Create your views here.

###############################################################################
class StockFilterView(TemplateView):

    template_name = 'stock/stockFilter.html'

    def get_context_data(self, **kwargs):

        context = super(StockFilterView, self).get_context_data(**kwargs)

        df = pd.read_csv('stockgetweb/crawl/test.csv')
        context.update({'stockData': df.to_html()})

        return context
###############################################################################
