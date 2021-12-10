INSERT INTO layer2_pallet.pl_task_type(
            task_type, ts_map)
    VALUES ('mp', 'multi_point_task');

INSERT INTO layer4_1_om.interaction_info_type(
            id, name, description)
    VALUES (1, 'check point load', 'check 取货交互');

INSERT INTO layer4_1_om.interaction_info_type(
            id, name, description)
    VALUES (2, 'i', '是否继续交互');

INSERT INTO layer4_1_om.interaction_info_type(
            id, name, description)
    VALUES (3, 'load', '搬完交互');

INSERT INTO layer4_1_om.interaction_info_type(
            id, name, description)
    VALUES (4, 'check point unload', 'check 放货交互');

INSERT INTO layer4_1_om.interaction_info_type(
            id, name, description)
    VALUES (5, 'check point', '传送带check点交互');

INSERT INTO layer4_1_om.interaction_info_type(
            id, name, description)
    VALUES (6, 'unload', '放完交互');
