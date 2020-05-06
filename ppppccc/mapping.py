# product
product = {
  "properties": {
    "date": {
      "index": false,
      "type": "date"
    },
    "seller": {
      "type": "keyword",
      "fields": {
        "completion": {
          "analyzer": "standard",
          "type": "completion"
        }
      }
    },
    "sold_last_1_pop": {
      "type": "float"
    },
    "item_location_country": {
      "type": "keyword"
    },
    "gmv_2_to_last": {
      "index": false,
      "type": "double"
    },
    "sold_6_to_last": {
      "index": false,
      "type": "long"
    },
    "gmv_4_to_last": {
      "index": false,
      "type": "double"
    },
    "gmv_6_to_last": {
      "index": false,
      "type": "double"
    },
    "gmv_last_1_pop": {
      "type": "float"
    },
    "item_location": {
      "index": false,
      "type": "keyword"
    },
    "price": {
      "type": "float"
    },
    "brand": {
      "type": "keyword",
      "fields": {
        "completion": {
          "analyzer": "standard",
          "type": "completion"
        }
      }
    },
    "pre_gmv_last_7": {
      "index": false,
      "type": "double"
    },
    "sold_last_1": {
      "type": "long"
    },
    "marketplace": {
      "index": false,
      "type": "keyword"
    },
    "sold_last_3": {
      "type": "long"
    },
    "sold_last_7": {
      "type": "long"
    },
    "pre_gmv_last_1": {
      "index": false,
      "type": "double"
    },
    "pre_gmv_last_3": {
      "index": false,
      "type": "double"
    },
    "visit_last_3": {
      "index": false,
      "type": "long"
    },
    "visit_last_1": {
      "index": false,
      "type": "long"
    },
    "sold_2_to_last": {
      "index": false,
      "type": "long"
    },
    "sold_4_to_last": {
      "index": false,
      "type": "long"
    },
    "sold_7_to_last": {
      "index": false,
      "type": "long"
    },
    "img": {
      "index": false,
      "type": "keyword"
    },
    "new_last_1": {
      "type": "long"
    },
    "gen_time": {
      "type": "date"
    },
    "gmv_5_to_last": {
      "index": false,
      "type": "double"
    },
    "new_last_3": {
      "type": "long"
    },
    "title": {
      "type": "text",
      "fields": {
        "completion": {
          "type": "completion"
        }
      }
    },
    "visit_last_7": {
      "index": false,
      "type": "long"
    },
    "new_last_7": {
      "type": "long"
    },
    "gmv_7_to_last": {
      "index": false,
      "type": "double"
    },
    "sold_total": {
      "index": false,
      "type": "long"
    },
    "update_time": {
      "index": false,
      "type": "date"
    },
    "sold_last_7_pop": {
      "type": "float"
    },
    "category_id": {
      "type": "keyword"
    },
    "gmv_last_1": {
      "type": "double"
    },
    "gmv_last_7_pop": {
      "type": "float"
    },
    "gmv_last_3": {
      "type": "double"
    },
    "popular": {
      "index": false,
      "type": "boolean"
    },
    "store_location": {
      "type": "keyword"
    },
    "gmv_last_7": {
      "type": "double"
    },
    "item_id": {
      "type": "keyword"
    },
    "pre_sold_last_1": {
      "index": false,
      "type": "long"
    },
    "sold_last_3_pop": {
      "type": "float"
    },
    "pre_sold_last_3": {
      "index": false,
      "type": "long"
    },
    "gmv_last_3_pop": {
      "type": "float"
    },
    "store": {
      "type": "keyword"
    },
    "pre_sold_last_7": {
      "index": false,
      "type": "long"
    },
    "data_update_time": {
      "index": false,
      "type": "date"
    },
    "site": {
      "type": "keyword"
    },
    "@timestamp": {
      "type": "date"
    },
    "category_path": {
      "type": "text",
      "fields": {
        "completion": {
          "analyzer": "standard",
          "type": "completion"
        }
      }
    },
    "leaf_category_id": {
      "type": "keyword"
    },
    "sold_3_to_last": {
      "index": false,
      "type": "long"
    },
    "visit_total": {
      "index": false,
      "type": "long"
    },
    "sold_5_to_last": {
      "index": false,
      "type": "long"
    },
    "gmv_3_to_last": {
      "index": false,
      "type": "double"
    }
  }
}

# category
{
    "mappings": {
        "properties": {
            "@timestamp": {
                "type": "date"
            },
            "category_id": {
                "type": "keyword"
            },
            "gmv_last_1_pop": {
                "type": "float"
            },
            "gmv_last_1_delta": {
                "type": "float"
            },
            "gmv_last_1": {
                "type": "long"
            },
            "sold_last_1": {
                "type": "long"
            },
            "sold_last_1_pop": {
                "type": "float"
            },
            "gmv_last_3_pop": {
                "type": "float"
            },
            "gmv_last_3": {
                "type": "long"
            },
            "sold_last_3": {
                "type": "long"
            },
            "sold_last_3_pop": {
                "type": "float"
            },
            "gmv_last_7_pop": {
                "type": "float"
            },
            "gmv_last_7": {
                "type": "long"
            },
            "sold_last_7": {
                "type": "long"
            },
            "sold_last_7_pop": {
                "type": "float"
            },
            "site": {
                "type": "keyword"
            },
            "date": {
                "type": "date"
            }
        }
    }
}

# brand
{
    "mappings": {
        "properties": {
            "@timestamp": {
                "type": "date"
            },
            "total_sold": {
                "type": "long"
            },
            "brand": {
                "type": "keyword"
            },
            "seller_count": {
                "type": "long"
            },
            "seller_count_delta": {
                "type": "long"
            },
            "sold_last_1": {
                "type": "long"
            },
            "sold_last_3": {
                "type": "long"
            },
            "sold_last_7": {
                "type": "long"
            },
            "sold_last_1_pop": {
                "type": "float"
            },
            "sold_last_3_pop": {
                "type": "float"
            },
            "sold_last_7_pop": {
                "type": "float"
            },
            "gmv_last_1": {
                "type": "long"
            },
            "gmv_last_3": {
                "type": "long"
            },
            "gmv_last_7": {
                "type": "long"
            },
            "gmv_last_1_pop": {
                "type": "float"
            },
            "gmv_last_3_pop": {
                "type": "float"
            },
            "gmv_last_7_pop": {
                "type": "float"
            },
            "avg_price_last_1": {
                "type": "float"
            },
            "avg_price_last_3": {
                "type": "float"
            },
            "avg_price_last_7": {
                "type": "float"
            },
            "avg_price_last_1_pop": {
                "type": "float"
            },
            "avg_price_last_3_pop": {
                "type": "float"
            },
            "avg_price_last_7_pop": {
                "type": "float"
            },
            "top_10_gmv": {
                "type": "float"
            },
            "top_10_gmv_pop": {
                "type": "float"
            },
            "new_last_1": {
                "type": "long"
            },
            "new_last_3": {
                "type": "long"
            },
            "new_last_7": {
                "type": "long"
            },
            "deal_last_1_pop": {
                "type": "float"
            },
            "deal_last_3_pop": {
                "type": "float"
            },
            "deal_last_7_pop": {
                "type": "float"
            },
            "site": {
                "type": "keyword"
            },
            "date": {
                "type": "date"
            }
        }
    }
}

# seller
{
    "mappings": {
        "properties": {
            "@timestamp": {
                "type": "date"
            },
            "sold_last_1": {
                "type": "long"
            },
            "sold_last_3": {
                "type": "long"
            },
            "sold_last_7": {
                "type": "long"
            },
            "sold_last_1_pop": {
                "type": "float"
            },
            "sold_last_3_pop": {
                "type": "float"
            },
            "sold_last_7_pop": {
                "type": "float"
            },
            "gmv_last_1": {
                "type": "long"
            },
            "gmv_last_3": {
                "type": "long"
            },
            "gmv_last_7": {
                "type": "long"
            },
            "gmv_last_1_pop": {
                "type": "float"
            },
            "gmv_last_3_pop": {
                "type": "float"
            },
            "gmv_last_7_pop": {
                "type": "float"
            },
            "avg_price_last_1": {
                "type": "float"
            },
            "avg_price_last_3": {
                "type": "float"
            },
            "avg_price_last_7": {
                "type": "float"
            },
            "avg_price_last_1_pop": {
                "type": "float"
            },
            "avg_price_last_3_pop": {
                "type": "float"
            },
            "avg_price_last_7_pop": {
                "type": "float"
            },
            "cvr_last_1": {
                "type": "float"
            },
            "cvr_last_3": {
                "type": "float"
            },
            "cvr_last_7": {
                "type": "float"
            },
            "top_10_gmv": {
                "type": "float"
            },
            "top_10_gmv_pop": {
                "type": "float"
            },
            "new_last_1": {
                "type": "long"
            },
            "new_last_3": {
                "type": "long"
            },
            "new_last_7": {
                "type": "long"
            },
            "deal_last_1_pop": {
                "type": "float"
            },
            "deal_last_3_pop": {
                "type": "float"
            },
            "deal_last_7_pop": {
                "type": "float"
            },
            "seller": {
                "type": "keyword"
            },
            "site": {
                "type": "keyword"
            },
            "date": {
                "type": "date"
            }
        }
    }
}

# category_default
{"track_total_hits": true, "query": {"bool": {"filter": [{"term": {"site": "us"}}], "must": [], "must_not": []}
                                     },
 "size": 0, "aggs": {"category_history": {"terms": {"field": "leaf_category_id", "size": 400}, "aggs": {
    "data_bucket_sort": {"bucket_sort": {"sort": [{"sold_last_1": {"order": "desc"}}]}
                         },
    "seller_count": {
        "cardinality": {
            "field": "seller"}}, "sold_total": {"sum": {"field": "sold_total"}},
    "sold_last_1": {"sum": {"field": "sold_last_1"}}, "sold_last_3": {"sum": {"field": "sold_last_3"}},
    "sold_last_7": {
        "sum": {
            "field": "sold_last_7"}}, "pre_sold_last_1": {"sum": {"field": "pre_sold_last_1"
                                                                  }
                                                          },
    "pre_sold_last_3": {
        "sum": {"field": "pre_sold_last_3"}}, "pre_sold_last_7": {"sum": {
        "field": "pre_sold_last_7"
    }
    },
    "gmv_last_1": {"sum": {"field": "gmv_last_1"}}, "gmv_last_3": {"sum": {"field": "gmv_last_3"}
                                                                   },
    "gmv_last_7": {
        "sum": {
            "field": "gmv_last_7"}}, "pre_gmv_last_1": {"sum": {"field": "pre_gmv_last_1"}},
    "pre_gmv_last_3": {"sum": {"field": "pre_gmv_last_3"}}, "pre_gmv_last_7": {"sum": {"field": "pre_gmv_last_7"}},
    "sold_last_1_pop": {
        "bucket_script": {
            "buckets_path": {"tPreSold_1": "pre_sold_last_1", "tSold_1": "sold_last_1"
                             },
            "script": "(params.tSold_1 - params.tPreSold_1) / params.tPreSold_1"
        }
    },
    "sold_last_3_pop": {
        "bucket_script": {"buckets_path": {"tPreSold_3": "pre_sold_last_3", "tSold_3": "sold_last_3"},
                          "script": "(params.tSold_3 - params.tPreSold_3) / params.tPreSold_3"}},
    "sold_last_7_pop": {"bucket_script": {"buckets_path": {"tPreSold_7": "pre_sold_last_7", "tSold_7": "sold_last_7"},
                                          "script": "(params.tSold_7 - params.tPreSold_7) / params.tPreSold_7"}
                        },
    "gmv_last_1_pop": {
        "bucket_script": {
            "buckets_path": {"tPreGmv_1": "pre_gmv_last_1", "tGmv_1": "gmv_last_1"},
            "script": "(params.tGmv_1 - params.tPreGmv_1) / params.tPreGmv_1"
        }
    },
    "gmv_last_3_pop": {"bucket_script": {"buckets_path": {"tPreGmv_3": "pre_gmv_last_3", "tGmv_3": "gmv_last_3"},
                                         "script": "(params.tGmv_3 - params.tPreGmv_3) / params.tPreGmv_3"}},
    "gmv_last_7_pop": {
        "bucket_script": {
            "buckets_path": {"tPreGmv_7": "pre_gmv_last_7", "tGmv_7": "gmv_last_7"
                             },
            "script": "(params.tGmv_7 - params.tPreGmv_7) / params.tPreGmv_7"
        }
    },
    "new_last_1": {
        "sum": {"field": "new_last_1"}}, "new_last_3": {"sum": {
        "field": "new_last_3"
    }
    },
    "new_last_7": {"sum": {"field": "new_last_7"}},
    "deal_last_1": {
        "sum": {
            "script": {"source": "doc['sold_last_1'].value>0"
                       }
        }
    },
    "deal_last_3": {"sum": {"script": {"source": "doc['sold_last_3'].value>0"}}
                    },
    "deal_last_7": {
        "sum": {
            "script": {
                "source": "doc['sold_last_7'].value>0"
            }
        }
    },
    "pre_deal_last_1": {"sum": {"script": {"source": "doc['pre_sold_last_1'].value>0"}}},
    "pre_deal_last_3": {"sum": {"script": {"source": "doc['pre_sold_last_3'].value>0"}}},
    "pre_deal_last_7": {
        "sum": {
            "script": {"source": "doc['pre_sold_last_7'].value>0"}}}, "deal_last_1_pop": {
        "bucket_script": {"buckets_path": {"tDeal_1": "deal_last_1", "tPreDeal_1": "pre_deal_last_1"},
                          "script": "(params.tDeal_1 - params.tPreDeal_1) / params.tPreDeal_1"}}, "deal_last_3_pop": {
        "bucket_script": {
            "buckets_path": {"tDeal_3": "deal_last_3", "tPreDeal_3": "pre_deal_last_3"
                             },
            "script": "(params.tDeal_3 - params.tPreDeal_3) / params.tPreDeal_3"
        }
    }, "deal_last_7_pop": {
        "bucket_script": {"buckets_path": {"tDeal_7": "deal_last_7", "tPreDeal_7": "pre_deal_last_7"},
                          "script": "(params.tDeal_7 - params.tPreDeal_7) / params.tPreDeal_7"}},
    "sold_2_to_last": {"sum": {"field": "sold_2_to_last"}}, "sold_3_to_last": {"sum": {"field": "sold_3_to_last"}
                                                                               },
    "sold_4_to_last": {
        "sum": {
            "field": "sold_4_to_last"}}, "sold_5_to_last": {"sum": {"field": "sold_5_to_last"}},
    "sold_6_to_last": {"sum": {"field": "sold_6_to_last"}}, "sold_7_to_last": {"sum": {"field": "sold_7_to_last"}}}
                                          },
                     "sum_sold_total": {
                         "sum": {
                             "field": "sold_total"
                         }
                     },
                     "sum_sold_last_1": {
                         "sum": {"field": "sold_last_1"}},
                     "sum_sold_last_3": {"sum": {
                         "field": "sold_last_3"
                     }
                     },
                     "sum_sold_last_7": {"sum": {"field": "sold_last_7"}},
                     "sum_gmv_last_1": {
                         "sum": {
                             "field": "gmv_last_1"}
                     },
                     "sum_gmv_last_3": {
                         "sum": {
                             "field": "gmv_last_3"
                         }
                     },
                     "sum_gmv_last_7": {
                         "sum": {"field": "gmv_last_7"}},
                     "count": {"cardinality": {"field": "leaf_category_id"}}}}

# brand defalut
{"track_total_hits": true, "query": {"bool": {"filter": [{"term": {"site": "us"}}], "must": [], "must_not": []}
                                     },
 "aggs": {
     "brand_history": {
         "terms": {"field": "brand", "size": 400}, "aggs": {
             "data_bucket_sort": {
                 "bucket_sort": {"sort": [{"sold_last_1": {"order": "desc"}}]}
             },
             "new_top_10_gmv": {
                 "filter": {
                     "term": {"new_last_1": "1"}}, "aggs": {"top_10_gmv": {
                     "top_hits": {"sort": [{"gmv_last_1": {"order": "desc"}}], "_source": {
                         "includes": "gmv_last_1"
                     },
                                  "size": 10}}}}, "top_10_gmv": {
                 "top_hits": {"sort": [{"gmv_last_1": {"order": "desc"}}], "_source": {"includes": "gmv_last_1"},
                              "size": 10
                              }
             },
             "pre_top_10_gmv": {
                 "top_hits": {"sort": [{"pre_gmv_last_1": {"order": "desc"}}], "_source": {
                     "includes": "pre_gmv_last_1"
                 },
                              "size": 10}}, "sold_total": {"sum": {"field": "sold_total"}},
             "seller_count": {"cardinality": {"field": "seller"}}, "visit_last_1": {"sum": {"field": "visit_last_1"}},
             "visit_last_3": {
                 "sum": {
                     "field": "visit_last_3"}}, "visit_last_7": {"sum": {"field": "visit_last_7"
                                                                         }
                                                                 },
             "sold_last_1": {
                 "sum": {"field": "sold_last_1"}}, "sold_last_3": {"sum": {
                 "field": "sold_last_3"
             }
             },
             "sold_last_7": {"sum": {"field": "sold_last_7"}}, "pre_sold_last_1": {"sum": {"field": "pre_sold_last_1"}
                                                                                   },
             "pre_sold_last_3": {
                 "sum": {
                     "field": "pre_sold_last_3"}}, "pre_sold_last_7": {"sum": {"field": "pre_sold_last_7"}},
             "gmv_last_1": {"sum": {"field": "gmv_last_1"}}, "gmv_last_3": {"sum": {"field": "gmv_last_3"}},
             "gmv_last_7": {
                 "sum": {
                     "field": "gmv_last_7"}
             }, "sold_last_1_pop": {
                 "bucket_script": {
                     "buckets_path": {"tPreSold_1": "pre_sold_last_1", "tSold_1": "sold_last_1"},
                     "script": "(params.tSold_1 - params.tPreSold_1) / params.tPreSold_1"
                 }
             }, "sold_last_3_pop": {
                 "bucket_script": {"buckets_path": {"tPreSold_3": "pre_sold_last_3", "tSold_3": "sold_last_3"},
                                   "script": "(params.tSold_3 - params.tPreSold_3) / params.tPreSold_3"}},
             "sold_last_7_pop": {
                 "bucket_script": {
                     "buckets_path": {"tPreSold_7": "pre_sold_last_7", "tSold_7": "sold_last_7"
                                      },
                     "script": "(params.tSold_7 - params.tPreSold_7) / params.tPreSold_7"
                 }
             }, "gmv_last_1_pop": {
                 "bucket_script": {"buckets_path": {"tPreGmv_1": "pre_gmv_last_1", "tGmv_1": "gmv_last_1"},
                                   "script": "(params.tGmv_1 - params.tPreGmv_1) / params.tPreGmv_1"}},
             "gmv_last_3_pop": {
                 "bucket_script": {
                     "buckets_path": {
                         "tPreGmv_3": "pre_gmv_last_3", "tGmv_3": "gmv_last_3"},
                     "script": "(params.tGmv_3 - params.tPreGmv_3) / params.tPreGmv_3"}
             }, "gmv_last_7_pop": {
                 "bucket_script": {
                     "buckets_path": {"tPreGmv_7": "pre_gmv_last_7", "tGmv_7": "gmv_last_7"},
                     "script": "(params.tGmv_7 - params.tPreGmv_7) / params.tPreGmv_7"
                 }
             },
             "pre_gmv_last_1": {"sum": {"field": "pre_gmv_last_1"}},
             "pre_gmv_last_3": {"sum": {"field": "pre_gmv_last_3"}},
             "pre_gmv_last_7": {
                 "sum": {
                     "field": "pre_gmv_last_7"}}, "new_last_1": {"sum": {"field": "new_last_1"
                                                                         }
                                                                 },
             "new_last_3": {
                 "sum": {"field": "new_last_3"}}, "new_last_7": {"sum": {
                 "field": "new_last_7"
             }
             },
             "deal_last_1": {"sum": {"script": {"source": "doc['sold_last_1'].size()>0"}}},
             "deal_last_3": {"sum": {"script": {"source": "doc['sold_last_3'].size()>0"}}},
             "deal_last_7": {
                 "sum": {
                     "script": {"source": "doc['sold_last_7'].size()>0"
                                }
                 }
             },
             "pre_deal_last_1": {"sum": {"script": {"source": "doc['pre_sold_last_1'].size()>0"}}
                                 },
             "pre_deal_last_3": {
                 "sum": {
                     "script": {
                         "source": "doc['pre_sold_last_3'].size()>0"
                     }
                 }
             },
             "pre_deal_last_7": {"sum": {"script": {"source": "doc['pre_sold_last_7'].size()>0"}}}, "cvr_last_1": {
                 "bucket_script": {"buckets_path": {"tSold_1": "sold_last_1", "tVisit_1": "visit_last_1"},
                                   "script": "params.tSold_1 / params.tVisit_1"}}, "cvr_last_3": {
                 "bucket_script": {
                     "buckets_path": {
                         "tSold_3": "sold_last_3", "tVisit_3": "visit_last_3"},
                     "script": "params.tSold_3 / params.tVisit_3"}
             }, "cvr_last_7": {
                 "bucket_script": {
                     "buckets_path": {"tSold_7": "sold_last_7", "tVisit_7": "visit_last_7"},
                     "script": "params.tSold_7 / params.tVisit_7"
                 }
             },
             "sold_2_to_last": {"sum": {"field": "sold_2_to_last"}},
             "sold_3_to_last": {"sum": {"field": "sold_3_to_last"}},
             "sold_4_to_last": {
                 "sum": {
                     "field": "sold_4_to_last"}}, "sold_5_to_last": {"sum": {"field": "sold_5_to_last"
                                                                             }
                                                                     },
             "sold_6_to_last": {
                 "sum": {"field": "sold_6_to_last"}}, "sold_7_to_last": {"sum": {"field": "sold_7_to_last"}}}},
     "count": {
         "cardinality": {
             "field": "brand"}}, "sum_sold_total": {"sum": {"field": "sold_total"
                                                            }
                                                    },
     "sum_sold_last_1": {
         "sum": {"field": "sold_last_1"}}, "sum_sold_last_3": {"sum": {
         "field": "sold_last_3"
     }
     },
     "sum_sold_last_7": {"sum": {"field": "sold_last_7"}}, "sum_gmv_last_1": {"sum": {"field": "gmv_last_1"}
                                                                              },
     "sum_gmv_last_3": {
         "sum": {
             "field": "gmv_last_3"}}, "sum_gmv_last_7": {"sum": {"field": "gmv_last_7"}}}}

# seller defalut
{"track_total_hits": true, "query": {"bool": {"filter": [{"term": {"site": "us"}}], "must": [], "must_not": []}
                                     },
 "aggs": {
     "seller_history": {
         "terms": {"field": "seller", "size": 400}, "aggs": {
             "data_bucket_sort": {
                 "bucket_sort": {"sort": [{"sold_last_1": {"order": "desc"}}]}
             }, "cvr_last_1": {
                 "bucket_script": {
                     "buckets_path": {"tSold_1": "sold_last_1", "tVisit_1": "visit_last_1"},
                     "script": "params.tSold_1 / params.tVisit_1"
                 }
             }, "cvr_last_3": {
                 "bucket_script": {"buckets_path": {"tSold_3": "sold_last_3", "tVisit_3": "visit_last_3"},
                                   "script": "params.tSold_3 / params.tVisit_3"}}, "cvr_last_7": {
                 "bucket_script": {
                     "buckets_path": {"tSold_7": "sold_last_7", "tVisit_7": "visit_last_7"
                                      },
                     "script": "params.tSold_7 / params.tVisit_7"
                 }
             }, "cvr_total": {
                 "bucket_script": {"buckets_path": {"tSold_total": "sold_total", "tVisit_total": "visit_total"},
                                   "script": "params.tSold_total / params.tVisit_total"}},
             "new_top_10_gmv": {"filter": {"term": {"new_last_1": "1"}}, "aggs": {"top_10_gmv": {
                 "top_hits": {"sort": [{"gmv_last_1": {"order": "desc"}}], "_source": {
                     "includes": "gmv_last_1"
                 },
                              "size": 10}}}}, "top_10_gmv": {
                 "top_hits": {"sort": [{"gmv_last_1": {"order": "desc"}}], "_source": {"includes": "gmv_last_1"},
                              "size": 10
                              }
             },
             "pre_top_10_gmv": {
                 "top_hits": {"sort": [{"pre_gmv_last_1": {"order": "desc"}}], "_source": {
                     "includes": "pre_gmv_last_1"
                 },
                              "size": 10}}, "sold_total": {"sum": {"field": "sold_total"}},
             "visit_total": {"sum": {"field": "visit_total"}}, "visit_last_1": {"sum": {"field": "visit_last_1"}},
             "visit_last_3": {
                 "sum": {
                     "field": "visit_last_3"}}, "visit_last_7": {"sum": {"field": "visit_last_7"
                                                                         }
                                                                 },
             "sold_last_1": {
                 "sum": {"field": "sold_last_1"}}, "sold_last_3": {"sum": {
                 "field": "sold_last_3"
             }
             },
             "sold_last_7": {"sum": {"field": "sold_last_7"}}, "pre_sold_last_1": {"sum": {"field": "pre_sold_last_1"}
                                                                                   },
             "pre_sold_last_3": {
                 "sum": {
                     "field": "pre_sold_last_3"}}, "pre_sold_last_7": {"sum": {"field": "pre_sold_last_7"}},
             "gmv_last_1": {"sum": {"field": "gmv_last_1"}}, "gmv_last_3": {"sum": {"field": "gmv_last_3"}},
             "gmv_last_7": {
                 "sum": {
                     "field": "gmv_last_7"}}, "pre_gmv_last_1": {"sum": {"field": "pre_gmv_last_1"
                                                                         }
                                                                 },
             "pre_gmv_last_3": {
                 "sum": {"field": "pre_gmv_last_3"}}, "pre_gmv_last_7": {"sum": {
                 "field": "pre_gmv_last_7"
             }
             },
             "sold_last_1_pop": {
                 "bucket_script": {"buckets_path": {"tPreSold_1": "pre_sold_last_1", "tSold_1": "sold_last_1"},
                                   "script": "(params.tSold_1 - params.tPreSold_1) / params.tPreSold_1"}
             },
             "sold_last_3_pop": {
                 "bucket_script": {
                     "buckets_path": {"tPreSold_3": "pre_sold_last_3", "tSold_3": "sold_last_3"},
                     "script": "(params.tSold_3 - params.tPreSold_3) / params.tPreSold_3"
                 }
             },
             "sold_last_7_pop": {
                 "bucket_script": {"buckets_path": {"tPreSold_7": "pre_sold_last_7", "tSold_7": "sold_last_7"},
                                   "script": "(params.tSold_7 - params.tPreSold_7) / params.tPreSold_7"}},
             "gmv_last_1_pop": {
                 "bucket_script": {
                     "buckets_path": {"tPreGmv_1": "pre_gmv_last_1", "tGmv_1": "gmv_last_1"
                                      },
                     "script": "(params.tGmv_1 - params.tPreGmv_1) / params.tPreGmv_1"
                 }
             },
             "gmv_last_3_pop": {
                 "bucket_script": {"buckets_path": {"tPreGmv_3": "pre_gmv_last_3", "tGmv_3": "gmv_last_3"},
                                   "script": "(params.tGmv_3 - params.tPreGmv_3) / params.tPreGmv_3"}},
             "gmv_last_7_pop": {
                 "bucket_script": {"buckets_path": {"tPreGmv_7": "pre_gmv_last_7", "tGmv_7": "gmv_last_7"},
                                   "script": "(params.tGmv_7 - params.tPreGmv_7) / params.tPreGmv_7"}
             },
             "new_last_1": {
                 "sum": {
                     "field": "new_last_1"}}, "new_last_3": {"sum": {"field": "new_last_3"}},
             "new_last_7": {"sum": {
                 "field": "new_last_7"
             }
             },
             "deal_last_1": {"sum": {"script": {"source": "doc['sold_last_1'].value>0"}}},
             "deal_last_3": {"sum": {"script": {"source": "doc['sold_last_3'].value>0"}}},
             "deal_last_7": {
                 "sum": {
                     "script": {"source": "doc['sold_last_7'].value>0"
                                }
                 }
             },
             "pre_deal_last_1": {"sum": {"script": {"source": "doc['pre_sold_last_1'].value>0"}}
                                 },
             "pre_deal_last_3": {
                 "sum": {
                     "script": {
                         "source": "doc['pre_sold_last_3'].value>0"
                     }
                 }
             },
             "pre_deal_last_7": {"sum": {"script": {"source": "doc['pre_sold_last_7'].value>0"}}}, "deal_last_1_pop": {
                 "bucket_script": {"buckets_path": {"tDeal_1": "deal_last_1", "tPreDeal_1": "pre_deal_last_1"},
                                   "script": "(params.tDeal_1 - params.tPreDeal_1) / params.tPreDeal_1"}},
             "deal_last_3_pop": {
                 "bucket_script": {
                     "buckets_path": {
                         "tDeal_3": "deal_last_3", "tPreDeal_3": "pre_deal_last_3"},
                     "script": "(params.tDeal_3 - params.tPreDeal_3) / params.tPreDeal_3"}
             }, "deal_last_7_pop": {
                 "bucket_script": {
                     "buckets_path": {"tDeal_7": "deal_last_7", "tPreDeal_7": "pre_deal_last_7"},
                     "script": "(params.tDeal_7 - params.tPreDeal_7) / params.tPreDeal_7"
                 }
             },
             "sold_2_to_last": {"sum": {"field": "sold_2_to_last"}},
             "sold_3_to_last": {"sum": {"field": "sold_3_to_last"}},
             "sold_4_to_last": {
                 "sum": {
                     "field": "sold_4_to_last"}}, "sold_5_to_last": {"sum": {"field": "sold_5_to_last"
                                                                             }
                                                                     },
             "sold_6_to_last": {
                 "sum": {"field": "sold_6_to_last"}}, "sold_7_to_last": {"sum": {"field": "sold_7_to_last"}}}},
     "count": {
         "cardinality": {
             "field": "seller"}}, "sum_sold_total": {"sum": {"field": "sold_total"
                                                             }
                                                     },
     "sum_sold_last_1": {
         "sum": {"field": "sold_last_1"}}, "sum_sold_last_3": {"sum": {
         "field": "sold_last_3"
     }
     },
     "sum_sold_last_7": {"sum": {"field": "sold_last_7"}}, "sum_gmv_last_1": {"sum": {"field": "gmv_last_1"}
                                                                              },
     "sum_gmv_last_3": {
         "sum": {
             "field": "gmv_last_3"}}, "sum_gmv_last_7": {"sum": {
         "field": "gmv_last_7"
     }
     }
 }
 }
