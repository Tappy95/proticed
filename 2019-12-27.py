print("是否有关键词监控任务", select_task_info)
        if select_task_info != None:
            print("task表中有任务,根据参数查排名纪录")
            ids = [select_task_info['id']]
            # 默认查询当天的关键词排名记录
            start_time = (datetime.now()).strftime('%Y-%m-%d %H:%M:%S')
            end_time = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d %H:%M:%S')
            # 从数据库中获取参数

            # 向海鹰下发获取关键词排名监控记录
            result = GetAmazonKWMResult(
                ids=ids,
                start_time=start_time,
                end_time=end_time,
            ).request()
            # 获取成功,解析json后持久化到DB
            if result and result['msg'] == 'success':
                print("获取关键词排名", result['result'])
                keyword_rank = KeywordRankInfo(result.get("result", []))
                for infos in keyword_rank.parsed_infos():
                    insert_stmt = insert(amazon_keyword_rank)
                    on_duplicate_key_stmt = insert_stmt.on_duplicate_key_update(
                        asin=insert_stmt.inserted.asin,
                        keyword=insert_stmt.inserted.keyword,
                        site=insert_stmt.inserted.site,
                        rank=insert_stmt.inserted.rank,
                        aid=insert_stmt.inserted.aid,
                        update_time=insert_stmt.inserted.update_time,
                    )
                    conn.execute(on_duplicate_key_stmt, infos)
                    print("更新amazon_rank成功")
        # task表中无此任务,发布新的监控排名任务
        # TODO:有bug,没找出来
        else:
            print("没有关键词任务,创建任务")
            asin_and_keywords = [{"asin": asin, "keyword": keyword}]
            num_of_days = 30
            monitoring_num = 4
            result_from_addtask = AddAmazonKWM(
                station=site,
                asin_and_keywords=asin_and_keywords,
                num_of_days=num_of_days,
                monitoring_num=monitoring_num,
            ).request()
            print("在HY创建监控任务", result_from_addtask)
            # 获取添加任务的ID,向海鹰获取监控商品信息
            if result_from_addtask and result_from_addtask["msg"] == "success":
                task_id = []
                for one_task in result_from_addtask['result']:
                    task_id.append(one_task['id'])
                asin_list_result = GetAmazonKWMStatus(
                    station=site,
                    capture_status=0,
                    ids=task_id,
                ).request()
                print("获取 任务ID", asin_list_result)
                if asin_list_result['msg'] == "success":
                    for total_task in asin_list_result['result']['list']:
                        keyword_taskinfo = KeywordTaskInfo()
                        print(total_task)
                        with engine.connect() as conn:
                            print(keyword_taskinfo.parse(total_task))
                            infos = keyword_taskinfo.parse(total_task)
                            insert_stmt = insert(amazon_keyword_task)
                            onduplicate_key_stmt = insert_stmt.on_duplicate_key_update(
                                id=insert_stmt.inserted.id,
                                asin=insert_stmt.inserted.asin,
                                keyword=insert_stmt.inserted.keyword,
                                status=insert_stmt.inserted.status,
                                monitoring_num=insert_stmt.inserted.monitoring_num,
                                monitoring_count=insert_stmt.inserted.monitoring_count,
                                monitoring_type=insert_stmt.inserted.monitoring_type,
                                station=insert_stmt.inserted.station,
                                start_time=insert_stmt.inserted.start_time,
                                end_time=insert_stmt.inserted.end_time,
                                created_at=insert_stmt.inserted.created_at,
                                deleted_at=insert_stmt.inserted.deleted_at,
                                is_add=insert_stmt.inserted.start_time,
                                last_update=insert_stmt.inserted.last_update,
                            )
                            conn.execute(onduplicate_key_stmt, infos)
                    print("更新amazon_task成功")
                    # 通过参数发任务更新rank
                    ids = [asin_list_result['result']['list'][0]['id']]
                    # 默认查询当天的关键词排名记录
                    start_time = (datetime.now()).strftime('%Y-%m-%d %H:%M:%S')
                    end_time = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d %H:%M:%S')
                    # 从数据库中获取参数
                    # 向海鹰下发获取关键词排名监控记录
                    result = GetAmazonKWMResult(
                        ids=ids,
                        start_time=start_time,
                        end_time=end_time,
                    ).request()
                    # 获取成功,解析后持久化到DB
                    if result and result['msg'] == 'success':
                        print("获取关键词排名", result['result'])
                        keyword_rank = KeywordRankInfo(result.get("result", []))
                        for infos in keyword_rank.parsed_infos():
                            insert_stmt = insert(amazon_keyword_rank)
                            on_duplicate_key_stmt = insert_stmt.on_duplicate_key_update(
                                asin=insert_stmt.inserted.asin,
                                keyword=insert_stmt.inserted.keyword,
                                site=insert_stmt.inserted.site,
                                rank=insert_stmt.inserted.rank,
                                aid=insert_stmt.inserted.aid,
                                update_time=insert_stmt.inserted.update_time,
                            )
                            conn.execute(on_duplicate_key_stmt, infos)
                            print("更新amazon_rank成功")