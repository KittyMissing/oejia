# coding=utf-8

init_sql = """
INSERT INTO "oe_shipper" (id, create_uid, code, create_date, name, write_uid, write_date) VALUES (1, 1, 'AJ', NOW() AT TIME ZONE 'UTC', '安捷快递', 1, NOW() AT TIME ZONE 'UTC') ON CONFLICT DO NOTHING;
INSERT INTO "oe_shipper" (id, create_uid, code, create_date, name, write_uid, write_date) VALUES (2, 1, 'ANE', NOW() AT TIME ZONE 'UTC', '安能物流', 1, NOW() AT TIME ZONE 'UTC') ON CONFLICT DO NOTHING;
INSERT INTO "oe_shipper" (id, create_uid, code, create_date, name, write_uid, write_date) VALUES (3, 1, 'AXD', NOW() AT TIME ZONE 'UTC', '安信达快递', 1, NOW() AT TIME ZONE 'UTC') ON CONFLICT DO NOTHING;
INSERT INTO "oe_shipper" (id, create_uid, code, create_date, name, write_uid, write_date) VALUES (4, 1, 'BQXHM', NOW() AT TIME ZONE 'UTC', '北青小红帽', 1, NOW() AT TIME ZONE 'UTC') ON CONFLICT DO NOTHING;
INSERT INTO "oe_shipper" (id, create_uid, code, create_date, name, write_uid, write_date) VALUES (5, 1, 'BFDF', NOW() AT TIME ZONE 'UTC', '百福东方', 1, NOW() AT TIME ZONE 'UTC') ON CONFLICT DO NOTHING;
INSERT INTO "oe_shipper" (id, create_uid, code, create_date, name, write_uid, write_date) VALUES (6, 1, 'BTWL', NOW() AT TIME ZONE 'UTC', '百世快运', 1, NOW() AT TIME ZONE 'UTC') ON CONFLICT DO NOTHING;
INSERT INTO "oe_shipper" (id, create_uid, code, create_date, name, write_uid, write_date) VALUES (7, 1, 'CCES', NOW() AT TIME ZONE 'UTC', 'CCES快递', 1, NOW() AT TIME ZONE 'UTC') ON CONFLICT DO NOTHING;
INSERT INTO "oe_shipper" (id, create_uid, code, create_date, name, write_uid, write_date) VALUES (8, 1, 'CITY100', NOW() AT TIME ZONE 'UTC', '城市100', 1, NOW() AT TIME ZONE 'UTC') ON CONFLICT DO NOTHING;
INSERT INTO "oe_shipper" (id, create_uid, code, create_date, name, write_uid, write_date) VALUES (9, 1, 'COE', NOW() AT TIME ZONE 'UTC', 'COE东方快递', 1, NOW() AT TIME ZONE 'UTC') ON CONFLICT DO NOTHING;
INSERT INTO "oe_shipper" (id, create_uid, code, create_date, name, write_uid, write_date) VALUES (10, 1, 'CSCY', NOW() AT TIME ZONE 'UTC', '长沙创一', 1, NOW() AT TIME ZONE 'UTC') ON CONFLICT DO NOTHING;
INSERT INTO "oe_shipper" (id, create_uid, code, create_date, name, write_uid, write_date) VALUES (11, 1, 'CDSTKY', NOW() AT TIME ZONE 'UTC', '成都善途速运', 1, NOW() AT TIME ZONE 'UTC') ON CONFLICT DO NOTHING;
INSERT INTO "oe_shipper" (id, create_uid, code, create_date, name, write_uid, write_date) VALUES (12, 1, 'DBL', NOW() AT TIME ZONE 'UTC', '德邦', 1, NOW() AT TIME ZONE 'UTC') ON CONFLICT DO NOTHING;
INSERT INTO "oe_shipper" (id, create_uid, code, create_date, name, write_uid, write_date) VALUES (13, 1, 'DSWL', NOW() AT TIME ZONE 'UTC', 'D速物流', 1, NOW() AT TIME ZONE 'UTC') ON CONFLICT DO NOTHING;
INSERT INTO "oe_shipper" (id, create_uid, code, create_date, name, write_uid, write_date) VALUES (14, 1, 'DTWL', NOW() AT TIME ZONE 'UTC', '大田物流', 1, NOW() AT TIME ZONE 'UTC') ON CONFLICT DO NOTHING;
INSERT INTO "oe_shipper" (id, create_uid, code, create_date, name, write_uid, write_date) VALUES (15, 1, 'EMS', NOW() AT TIME ZONE 'UTC', 'EMS', 1, NOW() AT TIME ZONE 'UTC') ON CONFLICT DO NOTHING;
INSERT INTO "oe_shipper" (id, create_uid, code, create_date, name, write_uid, write_date) VALUES (16, 1, 'FAST', NOW() AT TIME ZONE 'UTC', '快捷速递', 1, NOW() AT TIME ZONE 'UTC') ON CONFLICT DO NOTHING;
INSERT INTO "oe_shipper" (id, create_uid, code, create_date, name, write_uid, write_date) VALUES (17, 1, 'FEDEX', NOW() AT TIME ZONE 'UTC', 'FEDEX联邦(国内件）', 1, NOW() AT TIME ZONE 'UTC') ON CONFLICT DO NOTHING;
INSERT INTO "oe_shipper" (id, create_uid, code, create_date, name, write_uid, write_date) VALUES (18, 1, 'FEDEX_GJ', NOW() AT TIME ZONE 'UTC', 'FEDEX联邦(国际件）', 1, NOW() AT TIME ZONE 'UTC') ON CONFLICT DO NOTHING;
INSERT INTO "oe_shipper" (id, create_uid, code, create_date, name, write_uid, write_date) VALUES (19, 1, 'FKD', NOW() AT TIME ZONE 'UTC', '飞康达', 1, NOW() AT TIME ZONE 'UTC') ON CONFLICT DO NOTHING;
INSERT INTO "oe_shipper" (id, create_uid, code, create_date, name, write_uid, write_date) VALUES (20, 1, 'GDEMS', NOW() AT TIME ZONE 'UTC', '广东邮政', 1, NOW() AT TIME ZONE 'UTC') ON CONFLICT DO NOTHING;
INSERT INTO "oe_shipper" (id, create_uid, code, create_date, name, write_uid, write_date) VALUES (21, 1, 'GSD', NOW() AT TIME ZONE 'UTC', '共速达', 1, NOW() AT TIME ZONE 'UTC') ON CONFLICT DO NOTHING;
INSERT INTO "oe_shipper" (id, create_uid, code, create_date, name, write_uid, write_date) VALUES (22, 1, 'GTO', NOW() AT TIME ZONE 'UTC', '国通快递', 1, NOW() AT TIME ZONE 'UTC') ON CONFLICT DO NOTHING;
INSERT INTO "oe_shipper" (id, create_uid, code, create_date, name, write_uid, write_date) VALUES (23, 1, 'GTSD', NOW() AT TIME ZONE 'UTC', '高铁速递', 1, NOW() AT TIME ZONE 'UTC') ON CONFLICT DO NOTHING;
INSERT INTO "oe_shipper" (id, create_uid, code, create_date, name, write_uid, write_date) VALUES (24, 1, 'HFWL', NOW() AT TIME ZONE 'UTC', '汇丰物流', 1, NOW() AT TIME ZONE 'UTC') ON CONFLICT DO NOTHING;
INSERT INTO "oe_shipper" (id, create_uid, code, create_date, name, write_uid, write_date) VALUES (25, 1, 'HHTT', NOW() AT TIME ZONE 'UTC', '天天快递', 1, NOW() AT TIME ZONE 'UTC') ON CONFLICT DO NOTHING;
INSERT INTO "oe_shipper" (id, create_uid, code, create_date, name, write_uid, write_date) VALUES (26, 1, 'HLWL', NOW() AT TIME ZONE 'UTC', '恒路物流', 1, NOW() AT TIME ZONE 'UTC') ON CONFLICT DO NOTHING;
INSERT INTO "oe_shipper" (id, create_uid, code, create_date, name, write_uid, write_date) VALUES (27, 1, 'HOAU', NOW() AT TIME ZONE 'UTC', '天地华宇', 1, NOW() AT TIME ZONE 'UTC') ON CONFLICT DO NOTHING;
INSERT INTO "oe_shipper" (id, create_uid, code, create_date, name, write_uid, write_date) VALUES (28, 1, 'hq568', NOW() AT TIME ZONE 'UTC', '华强物流', 1, NOW() AT TIME ZONE 'UTC') ON CONFLICT DO NOTHING;
INSERT INTO "oe_shipper" (id, create_uid, code, create_date, name, write_uid, write_date) VALUES (29, 1, 'HTKY', NOW() AT TIME ZONE 'UTC', '百世快递', 1, NOW() AT TIME ZONE 'UTC') ON CONFLICT DO NOTHING;
INSERT INTO "oe_shipper" (id, create_uid, code, create_date, name, write_uid, write_date) VALUES (30, 1, 'HXLWL', NOW() AT TIME ZONE 'UTC', '华夏龙物流', 1, NOW() AT TIME ZONE 'UTC') ON CONFLICT DO NOTHING;
INSERT INTO "oe_shipper" (id, create_uid, code, create_date, name, write_uid, write_date) VALUES (31, 1, 'HYLSD', NOW() AT TIME ZONE 'UTC', '好来运快递', 1, NOW() AT TIME ZONE 'UTC') ON CONFLICT DO NOTHING;
INSERT INTO "oe_shipper" (id, create_uid, code, create_date, name, write_uid, write_date) VALUES (32, 1, 'JGSD', NOW() AT TIME ZONE 'UTC', '京广速递', 1, NOW() AT TIME ZONE 'UTC') ON CONFLICT DO NOTHING;
INSERT INTO "oe_shipper" (id, create_uid, code, create_date, name, write_uid, write_date) VALUES (33, 1, 'JIUYE', NOW() AT TIME ZONE 'UTC', '九曳供应链', 1, NOW() AT TIME ZONE 'UTC') ON CONFLICT DO NOTHING;
INSERT INTO "oe_shipper" (id, create_uid, code, create_date, name, write_uid, write_date) VALUES (34, 1, 'JJKY', NOW() AT TIME ZONE 'UTC', '佳吉快运', 1, NOW() AT TIME ZONE 'UTC') ON CONFLICT DO NOTHING;
INSERT INTO "oe_shipper" (id, create_uid, code, create_date, name, write_uid, write_date) VALUES (35, 1, 'JLDT', NOW() AT TIME ZONE 'UTC', '嘉里物流', 1, NOW() AT TIME ZONE 'UTC') ON CONFLICT DO NOTHING;
INSERT INTO "oe_shipper" (id, create_uid, code, create_date, name, write_uid, write_date) VALUES (36, 1, 'JTKD', NOW() AT TIME ZONE 'UTC', '捷特快递', 1, NOW() AT TIME ZONE 'UTC') ON CONFLICT DO NOTHING;
INSERT INTO "oe_shipper" (id, create_uid, code, create_date, name, write_uid, write_date) VALUES (37, 1, 'JXD', NOW() AT TIME ZONE 'UTC', '急先达', 1, NOW() AT TIME ZONE 'UTC') ON CONFLICT DO NOTHING;
INSERT INTO "oe_shipper" (id, create_uid, code, create_date, name, write_uid, write_date) VALUES (38, 1, 'JYKD', NOW() AT TIME ZONE 'UTC', '晋越快递', 1, NOW() AT TIME ZONE 'UTC') ON CONFLICT DO NOTHING;
INSERT INTO "oe_shipper" (id, create_uid, code, create_date, name, write_uid, write_date) VALUES (39, 1, 'JYM', NOW() AT TIME ZONE 'UTC', '加运美', 1, NOW() AT TIME ZONE 'UTC') ON CONFLICT DO NOTHING;
INSERT INTO "oe_shipper" (id, create_uid, code, create_date, name, write_uid, write_date) VALUES (40, 1, 'JYWL', NOW() AT TIME ZONE 'UTC', '佳怡物流', 1, NOW() AT TIME ZONE 'UTC') ON CONFLICT DO NOTHING;
INSERT INTO "oe_shipper" (id, create_uid, code, create_date, name, write_uid, write_date) VALUES (41, 1, 'KYWL', NOW() AT TIME ZONE 'UTC', '跨越物流', 1, NOW() AT TIME ZONE 'UTC') ON CONFLICT DO NOTHING;
INSERT INTO "oe_shipper" (id, create_uid, code, create_date, name, write_uid, write_date) VALUES (42, 1, 'LB', NOW() AT TIME ZONE 'UTC', '龙邦快递', 1, NOW() AT TIME ZONE 'UTC') ON CONFLICT DO NOTHING;
INSERT INTO "oe_shipper" (id, create_uid, code, create_date, name, write_uid, write_date) VALUES (43, 1, 'LHT', NOW() AT TIME ZONE 'UTC', '联昊通速递', 1, NOW() AT TIME ZONE 'UTC') ON CONFLICT DO NOTHING;
INSERT INTO "oe_shipper" (id, create_uid, code, create_date, name, write_uid, write_date) VALUES (44, 1, 'MHKD', NOW() AT TIME ZONE 'UTC', '民航快递', 1, NOW() AT TIME ZONE 'UTC') ON CONFLICT DO NOTHING;
INSERT INTO "oe_shipper" (id, create_uid, code, create_date, name, write_uid, write_date) VALUES (45, 1, 'MLWL', NOW() AT TIME ZONE 'UTC', '明亮物流', 1, NOW() AT TIME ZONE 'UTC') ON CONFLICT DO NOTHING;
INSERT INTO "oe_shipper" (id, create_uid, code, create_date, name, write_uid, write_date) VALUES (46, 1, 'NEDA', NOW() AT TIME ZONE 'UTC', '能达速递', 1, NOW() AT TIME ZONE 'UTC') ON CONFLICT DO NOTHING;
INSERT INTO "oe_shipper" (id, create_uid, code, create_date, name, write_uid, write_date) VALUES (47, 1, 'PADTF', NOW() AT TIME ZONE 'UTC', '平安达腾飞快递', 1, NOW() AT TIME ZONE 'UTC') ON CONFLICT DO NOTHING;
INSERT INTO "oe_shipper" (id, create_uid, code, create_date, name, write_uid, write_date) VALUES (48, 1, 'QCKD', NOW() AT TIME ZONE 'UTC', '全晨快递', 1, NOW() AT TIME ZONE 'UTC') ON CONFLICT DO NOTHING;
INSERT INTO "oe_shipper" (id, create_uid, code, create_date, name, write_uid, write_date) VALUES (49, 1, 'QFKD', NOW() AT TIME ZONE 'UTC', '全峰快递', 1, NOW() AT TIME ZONE 'UTC') ON CONFLICT DO NOTHING;
INSERT INTO "oe_shipper" (id, create_uid, code, create_date, name, write_uid, write_date) VALUES (50, 1, 'QRT', NOW() AT TIME ZONE 'UTC', '全日通快递', 1, NOW() AT TIME ZONE 'UTC') ON CONFLICT DO NOTHING;
INSERT INTO "oe_shipper" (id, create_uid, code, create_date, name, write_uid, write_date) VALUES (51, 1, 'RFD', NOW() AT TIME ZONE 'UTC', '如风达', 1, NOW() AT TIME ZONE 'UTC') ON CONFLICT DO NOTHING;
INSERT INTO "oe_shipper" (id, create_uid, code, create_date, name, write_uid, write_date) VALUES (52, 1, 'SAD', NOW() AT TIME ZONE 'UTC', '赛澳递', 1, NOW() AT TIME ZONE 'UTC') ON CONFLICT DO NOTHING;
INSERT INTO "oe_shipper" (id, create_uid, code, create_date, name, write_uid, write_date) VALUES (53, 1, 'SAWL', NOW() AT TIME ZONE 'UTC', '圣安物流', 1, NOW() AT TIME ZONE 'UTC') ON CONFLICT DO NOTHING;
INSERT INTO "oe_shipper" (id, create_uid, code, create_date, name, write_uid, write_date) VALUES (54, 1, 'SBWL', NOW() AT TIME ZONE 'UTC', '盛邦物流', 1, NOW() AT TIME ZONE 'UTC') ON CONFLICT DO NOTHING;
INSERT INTO "oe_shipper" (id, create_uid, code, create_date, name, write_uid, write_date) VALUES (55, 1, 'SDWL', NOW() AT TIME ZONE 'UTC', '上大物流', 1, NOW() AT TIME ZONE 'UTC') ON CONFLICT DO NOTHING;
INSERT INTO "oe_shipper" (id, create_uid, code, create_date, name, write_uid, write_date) VALUES (56, 1, 'SF', NOW() AT TIME ZONE 'UTC', '顺丰快递', 1, NOW() AT TIME ZONE 'UTC') ON CONFLICT DO NOTHING;
INSERT INTO "oe_shipper" (id, create_uid, code, create_date, name, write_uid, write_date) VALUES (57, 1, 'SFWL', NOW() AT TIME ZONE 'UTC', '盛丰物流', 1, NOW() AT TIME ZONE 'UTC') ON CONFLICT DO NOTHING;
INSERT INTO "oe_shipper" (id, create_uid, code, create_date, name, write_uid, write_date) VALUES (58, 1, 'SHWL', NOW() AT TIME ZONE 'UTC', '盛辉物流', 1, NOW() AT TIME ZONE 'UTC') ON CONFLICT DO NOTHING;
INSERT INTO "oe_shipper" (id, create_uid, code, create_date, name, write_uid, write_date) VALUES (59, 1, 'ST', NOW() AT TIME ZONE 'UTC', '速通物流', 1, NOW() AT TIME ZONE 'UTC') ON CONFLICT DO NOTHING;
INSERT INTO "oe_shipper" (id, create_uid, code, create_date, name, write_uid, write_date) VALUES (60, 1, 'STO', NOW() AT TIME ZONE 'UTC', '申通快递', 1, NOW() AT TIME ZONE 'UTC') ON CONFLICT DO NOTHING;
INSERT INTO "oe_shipper" (id, create_uid, code, create_date, name, write_uid, write_date) VALUES (61, 1, 'STWL', NOW() AT TIME ZONE 'UTC', '速腾快递', 1, NOW() AT TIME ZONE 'UTC') ON CONFLICT DO NOTHING;
INSERT INTO "oe_shipper" (id, create_uid, code, create_date, name, write_uid, write_date) VALUES (62, 1, 'SURE', NOW() AT TIME ZONE 'UTC', '速尔快递', 1, NOW() AT TIME ZONE 'UTC') ON CONFLICT DO NOTHING;
INSERT INTO "oe_shipper" (id, create_uid, code, create_date, name, write_uid, write_date) VALUES (63, 1, 'TSSTO', NOW() AT TIME ZONE 'UTC', '唐山申通', 1, NOW() AT TIME ZONE 'UTC') ON CONFLICT DO NOTHING;
INSERT INTO "oe_shipper" (id, create_uid, code, create_date, name, write_uid, write_date) VALUES (64, 1, 'UAPEX', NOW() AT TIME ZONE 'UTC', '全一快递', 1, NOW() AT TIME ZONE 'UTC') ON CONFLICT DO NOTHING;
INSERT INTO "oe_shipper" (id, create_uid, code, create_date, name, write_uid, write_date) VALUES (65, 1, 'UC', NOW() AT TIME ZONE 'UTC', '优速快递', 1, NOW() AT TIME ZONE 'UTC') ON CONFLICT DO NOTHING;
INSERT INTO "oe_shipper" (id, create_uid, code, create_date, name, write_uid, write_date) VALUES (66, 1, 'WJWL', NOW() AT TIME ZONE 'UTC', '万家物流', 1, NOW() AT TIME ZONE 'UTC') ON CONFLICT DO NOTHING;
INSERT INTO "oe_shipper" (id, create_uid, code, create_date, name, write_uid, write_date) VALUES (67, 1, 'WXWL', NOW() AT TIME ZONE 'UTC', '万象物流', 1, NOW() AT TIME ZONE 'UTC') ON CONFLICT DO NOTHING;
INSERT INTO "oe_shipper" (id, create_uid, code, create_date, name, write_uid, write_date) VALUES (68, 1, 'XBWL', NOW() AT TIME ZONE 'UTC', '新邦物流', 1, NOW() AT TIME ZONE 'UTC') ON CONFLICT DO NOTHING;
INSERT INTO "oe_shipper" (id, create_uid, code, create_date, name, write_uid, write_date) VALUES (69, 1, 'XFEX', NOW() AT TIME ZONE 'UTC', '信丰快递', 1, NOW() AT TIME ZONE 'UTC') ON CONFLICT DO NOTHING;
INSERT INTO "oe_shipper" (id, create_uid, code, create_date, name, write_uid, write_date) VALUES (70, 1, 'XYT', NOW() AT TIME ZONE 'UTC', '希优特', 1, NOW() AT TIME ZONE 'UTC') ON CONFLICT DO NOTHING;
INSERT INTO "oe_shipper" (id, create_uid, code, create_date, name, write_uid, write_date) VALUES (71, 1, 'XJ', NOW() AT TIME ZONE 'UTC', '新杰物流', 1, NOW() AT TIME ZONE 'UTC') ON CONFLICT DO NOTHING;
INSERT INTO "oe_shipper" (id, create_uid, code, create_date, name, write_uid, write_date) VALUES (72, 1, 'YADEX', NOW() AT TIME ZONE 'UTC', '源安达快递', 1, NOW() AT TIME ZONE 'UTC') ON CONFLICT DO NOTHING;
INSERT INTO "oe_shipper" (id, create_uid, code, create_date, name, write_uid, write_date) VALUES (73, 1, 'YCWL', NOW() AT TIME ZONE 'UTC', '远成物流', 1, NOW() AT TIME ZONE 'UTC') ON CONFLICT DO NOTHING;
INSERT INTO "oe_shipper" (id, create_uid, code, create_date, name, write_uid, write_date) VALUES (74, 1, 'YD', NOW() AT TIME ZONE 'UTC', '韵达快递', 1, NOW() AT TIME ZONE 'UTC') ON CONFLICT DO NOTHING;
INSERT INTO "oe_shipper" (id, create_uid, code, create_date, name, write_uid, write_date) VALUES (75, 1, 'YDH', NOW() AT TIME ZONE 'UTC', '义达国际物流', 1, NOW() AT TIME ZONE 'UTC') ON CONFLICT DO NOTHING;
INSERT INTO "oe_shipper" (id, create_uid, code, create_date, name, write_uid, write_date) VALUES (76, 1, 'YFEX', NOW() AT TIME ZONE 'UTC', '越丰物流', 1, NOW() AT TIME ZONE 'UTC') ON CONFLICT DO NOTHING;
INSERT INTO "oe_shipper" (id, create_uid, code, create_date, name, write_uid, write_date) VALUES (77, 1, 'YFHEX', NOW() AT TIME ZONE 'UTC', '原飞航物流', 1, NOW() AT TIME ZONE 'UTC') ON CONFLICT DO NOTHING;
INSERT INTO "oe_shipper" (id, create_uid, code, create_date, name, write_uid, write_date) VALUES (78, 1, 'YFSD', NOW() AT TIME ZONE 'UTC', '亚风快递', 1, NOW() AT TIME ZONE 'UTC') ON CONFLICT DO NOTHING;
INSERT INTO "oe_shipper" (id, create_uid, code, create_date, name, write_uid, write_date) VALUES (79, 1, 'YTKD', NOW() AT TIME ZONE 'UTC', '运通快递', 1, NOW() AT TIME ZONE 'UTC') ON CONFLICT DO NOTHING;
INSERT INTO "oe_shipper" (id, create_uid, code, create_date, name, write_uid, write_date) VALUES (80, 1, 'YTO', NOW() AT TIME ZONE 'UTC', '圆通速递', 1, NOW() AT TIME ZONE 'UTC') ON CONFLICT DO NOTHING;
INSERT INTO "oe_shipper" (id, create_uid, code, create_date, name, write_uid, write_date) VALUES (81, 1, 'YXKD', NOW() AT TIME ZONE 'UTC', '亿翔快递', 1, NOW() AT TIME ZONE 'UTC') ON CONFLICT DO NOTHING;
INSERT INTO "oe_shipper" (id, create_uid, code, create_date, name, write_uid, write_date) VALUES (82, 1, 'YZPY', NOW() AT TIME ZONE 'UTC', '邮政平邮/小包', 1, NOW() AT TIME ZONE 'UTC') ON CONFLICT DO NOTHING;
INSERT INTO "oe_shipper" (id, create_uid, code, create_date, name, write_uid, write_date) VALUES (83, 1, 'ZENY', NOW() AT TIME ZONE 'UTC', '增益快递', 1, NOW() AT TIME ZONE 'UTC') ON CONFLICT DO NOTHING;
INSERT INTO "oe_shipper" (id, create_uid, code, create_date, name, write_uid, write_date) VALUES (84, 1, 'ZHQKD', NOW() AT TIME ZONE 'UTC', '汇强快递', 1, NOW() AT TIME ZONE 'UTC') ON CONFLICT DO NOTHING;
INSERT INTO "oe_shipper" (id, create_uid, code, create_date, name, write_uid, write_date) VALUES (85, 1, 'ZJS', NOW() AT TIME ZONE 'UTC', '宅急送', 1, NOW() AT TIME ZONE 'UTC') ON CONFLICT DO NOTHING;
INSERT INTO "oe_shipper" (id, create_uid, code, create_date, name, write_uid, write_date) VALUES (86, 1, 'ZTE', NOW() AT TIME ZONE 'UTC', '众通快递', 1, NOW() AT TIME ZONE 'UTC') ON CONFLICT DO NOTHING;
INSERT INTO "oe_shipper" (id, create_uid, code, create_date, name, write_uid, write_date) VALUES (87, 1, 'ZTKY', NOW() AT TIME ZONE 'UTC', '中铁快运', 1, NOW() AT TIME ZONE 'UTC') ON CONFLICT DO NOTHING;
INSERT INTO "oe_shipper" (id, create_uid, code, create_date, name, write_uid, write_date) VALUES (88, 1, 'ZTO', NOW() AT TIME ZONE 'UTC', '中通速递', 1, NOW() AT TIME ZONE 'UTC') ON CONFLICT DO NOTHING;
INSERT INTO "oe_shipper" (id, create_uid, code, create_date, name, write_uid, write_date) VALUES (89, 1, 'ZTWL', NOW() AT TIME ZONE 'UTC', '中铁物流', 1, NOW() AT TIME ZONE 'UTC') ON CONFLICT DO NOTHING;
INSERT INTO "oe_shipper" (id, create_uid, code, create_date, name, write_uid, write_date) VALUES (90, 1, 'ZYWL', NOW() AT TIME ZONE 'UTC', '中邮物流', 1, NOW() AT TIME ZONE 'UTC') ON CONFLICT DO NOTHING;
INSERT INTO "oe_shipper" (id, create_uid, code, create_date, name, write_uid, write_date) VALUES (91, 1, 'AMAZON', NOW() AT TIME ZONE 'UTC', '亚马逊物流', 1, NOW() AT TIME ZONE 'UTC') ON CONFLICT DO NOTHING;
INSERT INTO "oe_shipper" (id, create_uid, code, create_date, name, write_uid, write_date) VALUES (92, 1, 'SUBIDA', NOW() AT TIME ZONE 'UTC', '速必达物流', 1, NOW() AT TIME ZONE 'UTC') ON CONFLICT DO NOTHING;
INSERT INTO "oe_shipper" (id, create_uid, code, create_date, name, write_uid, write_date) VALUES (93, 1, 'RFEX', NOW() AT TIME ZONE 'UTC', '瑞丰速递', 1, NOW() AT TIME ZONE 'UTC') ON CONFLICT DO NOTHING;
INSERT INTO "oe_shipper" (id, create_uid, code, create_date, name, write_uid, write_date) VALUES (94, 1, 'QUICK', NOW() AT TIME ZONE 'UTC', '快客快递', 1, NOW() AT TIME ZONE 'UTC') ON CONFLICT DO NOTHING;
INSERT INTO "oe_shipper" (id, create_uid, code, create_date, name, write_uid, write_date) VALUES (95, 1, 'CJKD', NOW() AT TIME ZONE 'UTC', '城际快递', 1, NOW() AT TIME ZONE 'UTC') ON CONFLICT DO NOTHING;
INSERT INTO "oe_shipper" (id, create_uid, code, create_date, name, write_uid, write_date) VALUES (96, 1, 'CNPEX', NOW() AT TIME ZONE 'UTC', 'CNPEX中邮快递', 1, NOW() AT TIME ZONE 'UTC') ON CONFLICT DO NOTHING;
INSERT INTO "oe_shipper" (id, create_uid, code, create_date, name, write_uid, write_date) VALUES (97, 1, 'HOTSCM', NOW() AT TIME ZONE 'UTC', '鸿桥供应链', 1, NOW() AT TIME ZONE 'UTC') ON CONFLICT DO NOTHING;
INSERT INTO "oe_shipper" (id, create_uid, code, create_date, name, write_uid, write_date) VALUES (98, 1, 'HPTEX', NOW() AT TIME ZONE 'UTC', '海派通物流公司', 1, NOW() AT TIME ZONE 'UTC') ON CONFLICT DO NOTHING;
INSERT INTO "oe_shipper" (id, create_uid, code, create_date, name, write_uid, write_date) VALUES (99, 1, 'AYCA', NOW() AT TIME ZONE 'UTC', '澳邮专线', 1, NOW() AT TIME ZONE 'UTC') ON CONFLICT DO NOTHING;
INSERT INTO "oe_shipper" (id, create_uid, code, create_date, name, write_uid, write_date) VALUES (100, 1, 'PANEX', NOW() AT TIME ZONE 'UTC', '泛捷快递', 1, NOW() AT TIME ZONE 'UTC') ON CONFLICT DO NOTHING;
INSERT INTO "oe_shipper" (id, create_uid, code, create_date, name, write_uid, write_date) VALUES (101, 1, 'PCA', NOW() AT TIME ZONE 'UTC', 'PCA Express', 1, NOW() AT TIME ZONE 'UTC') ON CONFLICT DO NOTHING;
INSERT INTO "oe_shipper" (id, create_uid, code, create_date, name, write_uid, write_date) VALUES (102, 1, 'UEQ', NOW() AT TIME ZONE 'UTC', 'UEQ Express', 1, NOW() AT TIME ZONE 'UTC') ON CONFLICT DO NOTHING;
"""
