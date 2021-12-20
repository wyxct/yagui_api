from ..base.dbcon.sqlserver import execute_commit_sql,run_sql,test_database_connection

class SQL:
    get_taskSJ = '''SELECT TRM_TaskSJ.TaskId, TRM_TaskSJ.TaskType, TRM_TaskSJ.Status, TRM_TaskSJ.Prority, TRM_TaskSJ.FromLoc, TRM_TaskSJ.ToLoc, TRM_TaskSJ.WHAreaId
    FROM TRM_TaskSJ WHERE  Status = '10' AND NOT EXISTS(SELECT 1 FROM TRM_Task_Sync_Status WHERE TaskId = TRM_TaskSJ.TaskId)
    AND TRM_TaskSJ.ToLoc IS NOT NULL AND TRM_TaskSJ.ToLoc != '';'''

    get_taskXJ = '''SELECT TRM_TaskXJ.TaskId, TRM_TaskXJ.TaskType, TRM_TaskXJ.Status, TRM_TaskXJ.Prority, TRM_TaskXJ.FromLoc, TRM_TaskXJ.ToLoc, 
    SOM_SyncOrder.Ex1 AS empty_pallet_exist, SOM_SyncOrder.Ex2 AS empty_pallet_pos, SOM_SyncOrder.Ex7 AS i_flag, TRM_TaskXJ.WHAreaId,
    SOM_SyncOrder.Ex10 AS empty_pallet_toloc
    FROM TRM_TaskXJ 
    LEFT JOIN SOM_SyncOrder ON TRM_TaskXJ.SourceBillId = SOM_SyncOrder.BillId
    WHERE TRM_TaskXJ.Status = '10' AND  NOT EXISTS(SELECT 1 FROM TRM_Task_Sync_Status WHERE TaskId = TRM_TaskXJ.TaskId)
    AND TRM_TaskXJ.ToLoc IS NOT NULL AND TRM_TaskXJ.ToLoc != '';'''

    get_taskOther = '''SELECT TRM_TaskOther.TaskId, TRM_TaskOther.TaskType, TRM_TaskOther.Status, TRM_TaskOther.Priority, TRM_TaskOther.FromLoc, TRM_TaskOther.ToLoc, WHAreaId, PalletCount
        FROM TRM_TaskOther
        WHERE Status = '10' AND
        NOT EXISTS(SELECT 1 FROM TRM_Task_Sync_Status WHERE TaskId = TRM_TaskOther.TaskId AND Status = 
        (CASE WHEN TaskType = '52' THEN '20' ELSE '10' END)
        ) AND TRM_TaskOther.ToLoc IS NOT NULL AND TRM_TaskOther.ToLoc != ''
        AND TRM_TaskOther.FromLoc IS NOT NULL AND TRM_TaskOther.FromLoc != '';'''

    get_taskOther_by_taskid = '''SELECT TaskType, PalletCount FROM TRM_TaskOther WHERE TaskId = '{TaskId}';'''

    insert_Task_Sync = '''
        INSERT INTO TRM_Task_Sync_Status (TaskId, Status, CreateBy, CreateDate) VALUES ( '{TaskId}', '{Status}', '{CreateBy}', GETDATE());'''

    update_Task_Sync = '''UPDATE TRM_Task_Sync_Status SET Status = '{Status}', OPT_By = '{OPT_By}', OPT_Date = GETDATE() WHERE TaskId = '{TaskId}';'''

    get_check_point = '''SELECT Property8 AS check_point FROM COM_Location WHERE LocationName = '{LocationName}';'''

    get_WHarea = '''SELECT Property5 FROM COM_WHArea WHERE WHAreaId = '{WHAreaId}';'''

    get_Empty_area = '''SELECT EmptyPalletGroupWHAreaId FROM COM_WHAreaRelation WHERE OutWHAreaId = '{WHAreaId}';'''

    # Property7:【取】 1)full:位置被托盘占据; 2)lock:位置预定，位置上仍有托盘; 3)empty:托盘被AGV搬走，空位状态;
    #           【放】1)empty:空位状态; 2)lock:位置预定，位置上没有托盘; 3)full:托盘被AGV放在位置上;
    # 取货优先级大的先取（靠近check点），卸货优先级小的开始卸（远离check点）{取卸货的优先级值一样}
    get_empty_pallet_loc = '''SELECT TOP 1 LocationName, Property6 AS CID FROM COM_Location WHERE 
WHAreaId IN (SELECT EmptyPalletGroupWHAreaId FROM COM_WHAreaRelation WHERE OutWHAreaId = '{WHAreaId}')
AND Property7 = 'full'
ORDER BY CAST (PickGoodsOrder AS INTEGER) DESC; '''

    # 卸货
    get_empty_loc = '''SELECT TOP 1 LocationName FROM COM_Location WHERE 
WHAreaId IN (SELECT WHAreaId FROM COM_Location WHERE LocationName = '{pos_loc}')
AND AisleId IN (SELECT AisleId FROM COM_Location WHERE LocationName = '{pos_loc}')
AND Property7 != 'full'
ORDER BY CAST (PutAwayOrder AS INTEGER); '''

    # 取货
    get_full_pallet_loc = '''SELECT TOP 1 LocationName FROM COM_Location WHERE 
    WHAreaId IN (SELECT WHAreaId FROM COM_Location WHERE LocationName = '{pos_loc}')
    AND AisleId IN (SELECT AisleId FROM COM_Location WHERE LocationName = '{pos_loc}')
    AND Property7 != 'empty'
    ORDER BY CAST (PickGoodsOrder AS INTEGER) DESC; '''

    # 空托垛卸货
    get_stack_empty_loc = '''SELECT TOP 1 LocationName FROM COM_Location WHERE 
    WHAreaId IN (SELECT WHAreaId FROM COM_Location WHERE LocationName = '{pos_loc}')
    AND AisleId IN (SELECT AisleId FROM COM_Location WHERE LocationName = '{pos_loc}')
    AND LLayer = 1
    AND Property7 != 'full'
    ORDER BY CAST (PutAwayOrder AS INTEGER); '''

    # 空托垛取货
    get_stack_full_pallet_loc = '''SELECT TOP 1 LocationName FROM COM_Location WHERE 
    WHAreaId IN (SELECT WHAreaId FROM COM_Location WHERE LocationName = '{pos_loc}')
    AND AisleId IN (SELECT AisleId FROM COM_Location WHERE LocationName = '{pos_loc}')
    AND LLayer = 1
    AND Property7 != 'empty'
    ORDER BY CAST (PickGoodsOrder AS INTEGER) DESC; '''
    
    get_empty_loc_in_trans = '''select LocationName from COM_Location WHERE LocationName in ('P1-01-01-01','P1-01-02-01') and Property7 = 'empty';'''

    update_location = '''UPDATE COM_Location SET Property7 = '{Status}', ModifyBy = '{OPT_By}', ModifyDate = GETDATE() WHERE LocationName = '{LocationName}' ;'''
    update_location_1 = '''UPDATE COM_Location SET Property7 = '{Status}', ModifyBy = '{OPT_By}', ModifyDate = GETDATE() WHERE LocationName in {LocationName} and Property7 = '{old_Status}' ;'''
    update_stack_location = '''UPDATE COM_Location SET Property7 = '{Status}', ModifyBy = '{OPT_By}', ModifyDate = GETDATE() WHERE GroupId = '{GroupId}' and LLayer <= {LLayer};'''

    get_loc_groupid = '''select GroupId from COM_Location where LocationName = '{LocationName}';'''
