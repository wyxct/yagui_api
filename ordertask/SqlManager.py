import json
from config import *

class InternalException(Exception):
    pass


class ExternalException(Exception):
    pass


class SQL:
    BATCH_INSERT = '''
        IF NOT EXISTS (SELECT 1 FROM dbo.COM_Batch WHERE BatchNo = %(BatchNo)s AND SkuId = %(SkuId)s AND StorerId = %(StorerId)s) AND SELECT 1 FROM COM_SKU WHERE StorerId=%(StorerId)s and SkuId=%(SkuId)s
    BEGIN
        INSERT INTO dbo.COM_Batch (BatchNo,BatchRuleId,SkuId,StorerId,IsSystem,Version,CreateBy,CreateDate)
        VALUES(%(BatchNo)s,'1',%(SkuId)s,%(StorerId)s,%(IsSystem)s,%(Version)s,%(CreateBy)s,%(CreateDate)s)
    END
    '''

    BATCH_DETAIL_INSERT = '''
        IF NOT EXISTS (SELECT 1 FROM dbo.COM_BatchDetail WHERE BatchNo = %(BatchNo)s AND SkuId = %(SkuId)s AND StorerId = %(StorerId)s AND AttribId = %(AttribId)s) AND SELECT 1 FROM COM_SKU WHERE StorerId=%(StorerId)s and SkuId=%(SkuId)s
    BEGIN
        INSERT INTO dbo.COM_BatchDetail (BatchNo,SkuId,StorerId,AttribId,AttribValue,Version,CreateBy,CreateDate)
        VALUES(%(BatchNo)s,%(SkuId)s,%(StorerId)s,%(AttribId)s,%(AttribValue)s,%(Version)s,%(CreateBy)s,%(CreateDate)s)
    END
    '''

    SKU_UPSERT = '''
        INSERT INTO dbo.COM_SKU (Version,CreateBy,StorerId,UDF01,SkuId,SkuName,CreateDate,UDF02,UDF03,CategoryId,UDF04,UDF07,GrossWeight,Weight,Unit,Length,Width,Height,PackageProperty,UDF05,UDF06,SkuType,Price,IsBom,IsSnMgt,IsLifeMgt,LifeCycle,RejectCycle)
        VALUES(%(Version)s,%(CreateBy)s,%(StorerId)s,%(UDF01)s,%(SkuId)s,%(SkuName)s,%(CreateDate)s,%(UDF02)s,%(UDF03)s,%(CategoryId)s,%(UDF04)s,%(UDF07)s,%(GrossWeight)s,%(Weight)s,%(Unit)s,%(Length)s,%(Width)s,%(Height)s,%(PackageProperty)s,%(UDF05)s,%(UDF06)s,%(SkuType)s,%(Price)s,%(IsBom)s,%(IsSnMgt)s,%(IsLifeMgt)s,%(LifeCycle)s,%(RejectCycle)s)
    '''

    SKUUPC_UPSERT = '''
        IF NOT EXISTS (SELECT 1 FROM dbo.COM_SKUUPC WHERE SkuId = %(SkuId)s)
    BEGIN
        INSERT INTO dbo.COM_SKUUPC (StorerId,SkuId,CreateDate,UpcCode,IsDefault,Version,CreateBy)
        VALUES(%(UDF01)s,%(SkuId)s,%(CreateDate)s,%(SkuId)s,%(IsDefault)s,%(Version)s,%(CreateBy)s)
    END
    '''

    STORER_UPSERT = '''
            IF NOT EXISTS (SELECT 1 FROM dbo.COM_Storer WHERE StorerId = %(StorerId)s)
        BEGIN
            INSERT INTO dbo.COM_Storer (StorerId,StorerName,Status,CreateBy,CreateDate,Version)
            VALUES(%(StorerId)s,%(StorerId)s,%(Status)s,%(CreateBy)s,%(CreateDate)s,%(Version)s)
        END
        '''

    SELECT_PICK_ORDER = '''
            SELECT * FROM dbo.SOM_Order WHERE SyncBillId = %(SyncBillId)s AND OrderType = %(OrderType)s AND BusinessType = %(BusinessType)s AND Status NOT IN('00','50','55')
    '''

    SELECT_ALL_PICK_ORDER = '''
            SELECT * FROM dbo.SOM_Order WHERE SyncBillId = %(SyncBillId)s AND Status NOT IN('00','50','55')
    '''

    SELECT_PICK_ORDER_DETAIL = '''
            SELECT A.BillId,OrderLineNo,SyncBillId,B.SkuId,SkuName,B.*,(SELECT ISNULL(CAST(SUM(SOM_ScanDetail.QtyOut)
             AS DECIMAL(18,4)),0) QtyOut FROM SOM_Scan,SOM_ScanDetail WHERE SOM_Scan.BillId=SOM_ScanDetail.BillId AND SOM_Scan.OrigBillId=A.BillId AND 
             SkuId =B.SkuId AND OrderLineNo = B.OrderLineNo) AS ScanQty FROM SOM_Order A INNER JOIN SOM_OrderDetail B ON A.BillId=B.BillId LEFT JOIN COM_SKU C ON B.SkuId = C.SkuId AND B.StorerId=C.StorerId 
             WHERE A.Status NOT IN('00','50','55') AND A.SyncBillId=%(SyncBillId)s ORDER BY A.SyncBillId DESC
    '''

    GET_CHINESE_STATUS = '''
            SELECT Name from dbo.COM_BaseCode where Code = %s and Type = 'SOM_OrderStatus'
    '''

    SELECT_PICK_SYNC_ORDER = '''
            SELECT VendorId,Ex1 FROM dbo.SOM_SyncOrder WHERE BillId = %(BillId)s
    '''

    SELECT_REPLEN_ORDER = '''
            SELECT * FROM dbo.SRM_Order WHERE SyncBillId = %(SyncBillId)s AND OrderType = %(OrderType)s AND BusinessType = %(BusinessType)s
    '''

    SELECT_REPLEN_ORDER_DETAIL = '''
        SELECT A.BillId,OrderLineNo,SyncBillId,B.SkuId,SkuName,B.*,(SELECT ISNULL(CAST(SUM(SRM_ScanDetail.QtyIn) AS DECIMAL(18,4)),0) QtyIn FROM SRM_Scan,SRM_ScanDetail WHERE SRM_Scan.BillId=SRM_ScanDetail.BillId AND SRM_Scan.OrigBillId=A.BillId AND SkuId =B.SkuId AND OrderLineNo = B.OrderLineNo) AS ScanQty 
        ,CarNo FROM SRM_Order A INNER JOIN SRM_OrderDetail B ON A.BillId=B.BillId LEFT JOIN COM_SKU C ON B.SkuId = C.SkuId AND B.StorerId=C.StorerId WHERE A.Status NOT IN('00','50','55') AND A.SyncBillId=%(SyncBillId)s ORDER BY A.SyncBillId DESC
    '''

    SELECT_MOVE = '''
            SELECT * FROM INV_BAL where WarehouseId = %(LGNUM)s AND LocationId = %(LGPLA)s AND SkuId = %(MATNR)s
        '''

    INSERT_REPLEN_ORDER = '''
        IF NOT EXISTS (SELECT 1 FROM dbo.SRM_Order WHERE SyncBillId = %(SyncBillId)s)
    BEGIN
        INSERT INTO dbo.SRM_Order (BillId,WarehouseId,InOutType,SyncBillDate,Status,OrigSystem,GoodsCount,SkuCount,IsCharge,BatchNo,Version,CreateBy,CreateDate,StorerId,OrderType,SyncBillId,OrigBillId,BusinessType,VendorId,CarNo,UDF01,UDF02)
        VALUES(%(BillId)s,%(WarehouseId)s,%(InOutType)s,%(SyncBillDate)s,%(Status)s,%(OrigSystem)s,%(GoodsCount)s,%(SkuCount)s,%(IsCharge)s,%(BatchNo)s,%(Version)s,%(CreateBy)s,%(CreateDate)s,%(StorerId)s,%(OrderType)s,%(SyncBillId)s,%(OrigBillId)s,%(BusinessType)s,%(VendorId)s,%(CarNo)s,%(VendorId)s,%(VendorName)s)
    END
    '''

    INSERT_REPLEN_ORDER_DETAIL = '''
        INSERT INTO dbo.SRM_OrderDetail (BillId,SkuStatus,PackageCode,PackageQty,Version,CreateBy,CreateDate,OrderLineNo,StorerId,SkuId,QtyPlan,BatchNo,ProductDate,ExpiryDate,UDF01,UDF02,UDF03,UDF04,UDF05,UDF06,UDF14,UDF15,UDF16,UDF17,UDF18)
        VALUES(%(BillId)s,%(SkuStatus)s,%(PackageCode)s,%(PackageQty)s,%(Version)s,%(CreateBy)s,%(CreateDate)s,%(OrderLineNo)s,%(StorerId)s,%(SkuId)s,%(QtyPlan)s,%(BatchNo)s,%(ProductDate)s,%(ExpiryDate)s,%(UDF01)s,%(UDF02)s,%(UDF03)s,%(UDF04)s,%(UDF05)s,%(UDF06)s,%(UDF14)s,%(UDF15)s,%(UDF16)s,%(UDF17)s,%(UDF18)s)
    '''

    INSERT_PICK_ORDER = '''
        IF NOT EXISTS (SELECT 1 FROM dbo.SOM_Order WHERE SyncBillId = %(SyncBillId)s)
    BEGIN
        INSERT INTO dbo.SOM_Order (BillId,StorerId,SyncBillId,SourceBillId,SOPType,Status,OrderSource,WarehouseId,OrderType,BusinessType,OrigSystem,Version,CreateBy,CreateDate)
        VALUES(%(BillId)s,%(StorerId)s,%(SyncBillId)s,%(SourceBillId)s,%(SOPType)s,%(BillStatus)s,%(OrderSource)s,%(WarehouseId)s,%(OrderType)s,%(BusinessType)s,%(OrigSystem)s,%(Version)s,%(CreateBy)s,%(CreateDate)s)
    END
    '''

    INSERT_PICK_SYNC_ORDER = '''
    IF NOT EXISTS (SELECT 1 FROM dbo.SOM_SyncOrder WHERE BillId = %(BillId)s)
    BEGIN
        INSERT INTO dbo.SOM_SyncOrder (BillId,SyncBillId,WarehouseId,StorerId,GoodsCount,SkuCount,Ex1)
        VALUES(%(BillId)s,%(SyncBillId)s,%(WarehouseId)s,%(StorerId)s,%(GoodsCount)s,%(SkuCount)s,%(CarNo)s)
    END
    '''

    INSERT_PICK_ORDER_DETAIL = '''
        INSERT INTO dbo.SOM_OrderDetail (UDF12.UDF13,OrderLineNo,BillId,StorerId,SkuId,SkuStatus,Qty,Unit,Status,BatchNo,ProductDate,ExpiryDate,PackageCode,PackageQty,Version,CreateBy,CreateDate,UDF01,UDF02,UDF03,UDF04,UDF05,UDF06,UDF15,UDF16,UDF17,UDF18,UDF19,Ex1,Ex2)
        VALUES(%(UDF12)s,%(UDF13)s,%(OrderLineNo)s,%(BillId)s,%(StorerId)s,%(SkuId)s,%(SkuStatus)s,%(Qty)s,%(Unit)s,%(Status)s,%(BatchNo)s,%(ProductDate)s,%(ExpiryDate)s,%(PackageCode)s,%(PackageQty)s,%(Version)s,%(CreateBy)s,%(CreateDate)s,%(UDF01)s,%(UDF02)s,%(UDF03)s,%(UDF04)s,%(Unit)s,%(UDF06)s,%(UDF15)s,%(UDF16)s,%(UDF17)s,%(UDF18)s,%(UDF19)s,%(Ex1)s,%(Ex2)s)
    '''

    FINISH_SJ_TASK = f'''
                    BEGIN
                DECLARE @issuccess int,@errmsg VARCHAR(100)
                SET @issuccess=1
                SET @errmsg = 'success'
                    EXEC SP_TRM_TaskSJ_Charge @TaskId = %(TaskId)s,@UserId = %(UserId)s,@ToLoc = %(ToLoc)s,@IP = %(IP)s,@ClientName = %(ClientName)s
                IF @@ERROR<>0
                BEGIN
                    SET @issuccess = 0
                    SET @errmsg = 'Insert Order ERROR!'
                END
                    SELECT @issuccess as issuccess,@errmsg as errmsg
                    RETURN
                END
            '''

    FINISH_XJ_TASK = '''
    BEGIN
                DECLARE @issuccess int,@errmsg VARCHAR(100)
                SET @issuccess=1
                SET @errmsg = 'success'
                    EXEC SP_TRM_TaskXJ_Charge @TaskId = %(TaskId)s,@UserId = %(UserId)s,@IP = %(IP)s,@ClientName = %(ClientName)s
                IF @@ERROR<>0
                BEGIN
                    SET @issuccess = 0
                    SET @errmsg = 'Insert Order ERROR!'
                END
                    SELECT @issuccess as issuccess,@errmsg as errmsg
                    RETURN
                END
    '''

    FINISH_OTHER_TASK = '''
            BEGIN
                DECLARE @issuccess int,@errmsg VARCHAR(100)
                SET @issuccess=1
                SET @errmsg = 'success'
                    UPDATE TRM_TaskOther SET Status='40',IsAgvCompleted=1,Version=Version+1,ModifyBy=%(UserId)s,ModifyDate=GETDATE() WHERE TaskId=%(TaskId)s AND Status='10'
                IF @@ERROR<>0
                BEGIN
                    SET @issuccess = 0
                    SET @errmsg = 'Insert Order ERROR!'
                END
                    SELECT @issuccess as issuccess,@errmsg as errmsg
                    RETURN
                END
    '''

    SELECT_TOP_REPLEN = '''
        SELECT TOP 10 * FROM SRM_Receipt A 
        WHERE A.Status IN('55') AND ISNULL(A.SyncBillId,'')<>'' AND A.OrderType IN('11','41','51','52') AND NOT EXISTS(SELECT * FROM SYS_Order_Sync_Status where OrderId = A.BillId) AND A.OrigSystem<>'MES'
    '''

    SELECT_REPLEN_POST_DETAIL1 = '''
        select c.BusinessType,c.WarehouseId,c.BillId,c.SyncBillId,b.OrderLineNo,b.UDF01,e.Property4 FromKCDD,f.Property4 ToKCDD,b.UDF15,
        b.SkuId,b.BatchNo,b.UDF14,c.StorerId,sum(b.QtyScan) QtyScan,b.UDF05,b.ProductDate,c.ChargeBy,c.OrderDate,b.UDF13
        from TRM_TaskSJ a inner join TRM_TaskSJDetail b on a.TaskId=b.TaskId 
        inner join SRM_Receipt c on c.OrigBillId=a.SourceBillId
        inner join SRM_Order o on (c.origbillid=o.BillId)
        inner join COM_Location e on a.FromLoc=e.LocationId
        inner join COM_Location f on a.ToLoc=f.LocationId
        where c.BillId=%s    
        group by c.BusinessType,c.WarehouseId,c.BillId,c.SyncBillId,b.OrderLineNo,b.UDF01,e.Property4,f.Property4,b.UDF15,
        b.SkuId,b.BatchNo,b.UDF14,c.StorerId,b.UDF05,b.ProductDate,c.ChargeBy,c.OrderDate,b.UDF13
    '''

    SELECT_REPLEN_POST_DETAIL2 = '''
        select c.WarehouseId,e.BillId,b.OrderLineNo,b.ToLoc,b.UDF06,sum(cast(b.UDF07 as decimal(18,4))) UDF07,sum(b.qtyscan) QtyScan,c.WHAreaId  
        from TRM_TaskSJ a 
        inner join TRM_TaskSJDetail b on a.TaskId=b.TaskId 
        inner join COM_Location c on a.ToLoc=c.LocationId
        inner join SRM_Order d on a.SourceBillId=d.BillId
        inner join SRM_Receipt e on d.BillId=e.OrigBillId
        where e.BillId=%s    
        GROUP BY c.WarehouseId,e.BillId,b.OrderLineNo,b.ToLoc,b.UDF06,c.WHAreaId
    '''

    SELECT_TOP_MATERIAL = '''
            SELECT TOP 10 * FROM SRM_Receipt A 
            WHERE A.Status IN('55') AND ISNULL(A.SyncBillId,'')<>'' AND NOT EXISTS(SELECT 1 FROM SYS_Order_Sync_Status WHERE OrderId=A.BillId)
            AND A.OrderType IN('41') and A.OrigSystem='MES'
        '''

    SELECT_MATERIAL_POST_DETAIL1 = '''
            select a.StorerId,o.UDF12 MUDF12,o.UDF13 MUDF13,o.UDF14 MUDF14,o.UDF15 MUDF15,o.UDF16 MUDF16,o.UDF17 MUDF17,o.UDF18 MUDF18,
            b.UDF15,c.ChargeBy,c.OrderDate
            from TRM_TaskSJ a inner join TRM_TaskSJDetail b on a.TaskId=b.TaskId 
            inner join SRM_Receipt c on c.OrigBillId=a.SourceBillId
            inner join SRM_Order o on (c.origbillid=o.BillId)
            where c.BillId=%s    
            group by a.StorerId,o.UDF12,o.UDF13,o.UDF14,o.UDF15,o.UDF16,o.UDF17,o.UDF18,b.UDF15,c.ChargeBy,c.OrderDate
        '''

    SELECT_MATERIAL_POST_DETAIL2 = '''
            select b.OrderLineNo,b.UDF01,b.UDF13,b.UDF15,b.SkuId,b.BatchNo,sum(b.QtyScan) QtyScan,
            c.BusinessType,c.WarehouseId,c.BillId, c.SkuCount,g.Ex1,g.Ex2,g.Ex8,g.Ex9,o.UDF12 MUDF12
            from TRM_TaskSJ a inner join TRM_TaskSJDetail b on a.TaskId=b.TaskId 
            inner join SRM_Receipt c on c.OrigBillId=a.SourceBillId
            inner join SRM_Order o on (c.origbillid=o.BillId)
            inner join SRM_OrderDetail g on(b.OrderId=g.BillId and b.OrderLineNo=g.OrderLineNo)
            where c.BillId=%s    
            group by b.OrderLineNo,b.UDF01,b.UDF13,b.UDF15,b.SkuId,b.BatchNo,
            c.BusinessType,c.WarehouseId,c.BillId, c.SkuCount,g.Ex1,g.Ex2,g.Ex8,g.Ex9,o.UDF12
        '''

    SELECT_MATERIAL_POST_DETAIL3 = '''
            select c.WarehouseId,e.BillId,b.OrderLineNo,b.ToLoc,b.UDF06,sum(cast(b.UDF07 as decimal(18,4))) UDF07,sum(b.qtyscan) QtyScan,c.WHAreaId  
            from TRM_TaskSJ a 
            inner join TRM_TaskSJDetail b on a.TaskId=b.TaskId 
            inner join COM_Location c on a.ToLoc=c.LocationId
            inner join SRM_Order d on a.SourceBillId=d.BillId
            inner join SRM_Receipt e on d.BillId=e.OrigBillId
            where e.BillId=%s    
            GROUP BY c.WarehouseId,e.BillId,b.OrderLineNo,b.ToLoc,b.UDF06,c.WHAreaId
        '''

    SELECT_TASK = '''
        SELECT B.*,C.Property7,D.UDF06,D.UDF07 FROM TRM_TaskSJ A INNER JOIN TRM_TaskSJDetail B ON A.TaskId=B.TaskId
        INNER JOIN COM_Location C ON B.ToLoc=C.LocationId
        INNER JOIN SRM_ReceiptDetail D ON (D.BillId=B.OrderId AND D.OrderLineNo=B.OrderLineNo AND D.SkuId=B.SkuId)
        WHERE A.SourceBillId=%(SourceBillId)s 
    '''

    UPDATE_RECEIPT_DETAIL = '''
        UPDATE SRM_ReceiptDetail SET UDF08=%(UDF08)s,UDF09=%(UDF09)s,UDF10=%(UDF10)s,UDF11=%(UDF11)s WHERE BillId=%(BillId)s and OrderLineNo=%(OrderLineNo)s
    '''

    UPDATE_RECEIPT_TASK = '''
        EXEC SP_SRM_Receipt_QMUpdate @BillId = %(BillId)s,@UserId = 'IO',@IP = '', @ClientName = ''
    '''

    RECEIPT_QMUPDATE = '''
       EXEC SP_SRM_Receipt_QMUpdate %(BillId)s,'SAP','',''
    '''

    SELECT_TOP_PICK = '''
        SELECT TOP 10 * FROM SOM_Issue A 
        WHERE A.Status IN('55') AND ISNULL(A.SyncBillId,'')<>'' AND NOT EXISTS(SELECT 1 FROM SYS_Order_Sync_Status WHERE OrderId=A.BillId) AND A.OrderType IN('21','31','51','52')
    '''

    SELECT_PICK_POST_DETAIL1 = '''
        select c.BusinessType,c.WarehouseId,c.BillId,c.SyncBillId,d.UDF12,d.UDF14,d.UDF20,d.UDF15,d.UDF16,d.UDF17,b.OrderLineNo,e.Property4 FromKCDD,f.Property4 ToKCDD,
        b.SkuId,b.BatchNo,c.StorerId,sum(b.QtyScan) QtyScan,b.UDF05,b.ProductDate,c.ChargeBy,c.OrderDate  
        from TRM_TaskXJ a inner join TRM_TaskXJDetail b on a.TaskId=b.TaskId 
        inner join SOM_Issue c on c.OrigBillId=a.SourceBillId
        inner join SOM_OrderDetail d on (d.BillId=a.SourceBillId and b.OrderLineNo=d.OrderLineNo and b.SkuId=d.SkuId)
        inner join COM_Location e on a.FromLoc=e.LocationId
        inner join COM_Location f on a.ToLoc=f.LocationId
        where c.BillId=%s
        group by c.BusinessType,c.WarehouseId,c.BillId,c.SyncBillId,d.UDF12,d.UDF14,d.UDF20,d.UDF15,d.UDF16,d.UDF17,b.OrderLineNo,e.Property4,f.Property4,
        b.SkuId,b.BatchNo,c.StorerId,b.UDF05,b.ProductDate,c.ChargeBy,c.OrderDate
    '''

    SELECT_PICK_POST_DETAIL2 = '''
        select c.WarehouseId,c.BillId,b.OrderLineNo,b.UDF06,b.UDF07,b.QtyScan,a.WHAreaId,a.FromLoc  
        from TRM_TaskXJ a inner join TRM_TaskXJDetail b on a.TaskId=b.TaskId 
        inner join SOM_Issue c on c.OrigBillId=a.SourceBillId
        where c.BillId=%s
    '''

    SELECT_PICK = '''
        SELECT B.* FROM SOM_Issue A INNER JOIN SOM_IssueDetail B ON A.BillId=B.BillId
        WHERE A.BillId=%(BillId)s
    '''

    SELECT_TASK_PICK = '''
        SELECT B.*,C.Property7 FROM TRM_TaskXJ A INNER JOIN TRM_TaskXJDetail B ON A.TaskId=B.TaskId
        INNER JOIN COM_Location C ON B.ToLoc=C.LocationId
        WHERE A.SourceBillId=%(SourceBillId)s
    '''

    SELECT_REPLEN_ORDER_TYPE = '''
        SELECT * FROM COM_BaseCode WHERE Type = 'SRM_OrderType' AND Code = %s
    '''

    SELECT_PICK_ORDER_TYPE = '''
        SELECT * FROM COM_BaseCode WHERE Type = 'SOM_OrderType' AND Code = %s
    '''

    SELECT_REPLEN_BUSINESS_TYPE = '''
        SELECT * FROM COM_BaseCode WHERE Type = 'SRMOrder_BusinessType' AND Code = %s
    '''

    SELECT_PICK_BUSINESS_TYPE = '''
        SELECT * FROM COM_BaseCode WHERE Type = 'SOMOrder_BusinessType' AND Code = %s
    '''

    INSERT_ADJUSTNOTIFY = '''
        IF NOT EXISTS (SELECT 1 FROM dbo.WRM_AdjustNotify WHERE BillId = %(BillId)s)
    BEGIN
        INSERT INTO dbo.WRM_AdjustNotify (BillId,WarehouseId,StorerId,OrigBillType,OrigBillId,OrderDate,Status,Version,CreateBy,CreateDate)
        VALUES(%(BillId)s,%(WarehouseId)s,%(StorerId)s,%(OrigBillType)s,%(OrigBillId)s,%(OrderDate)s,%(Status)s,%(Version)s,%(CreateBy)s,%(CreateDate)s)
    END
    '''

    INSERT_ADJUSTNOTIFY_DETAIL = '''
        INSERT INTO dbo.WRM_AdjustNotifyDetail (SkuStatus,LocationId,BillId,OrderLineNo,StorerId,SkuId,QtyPlan,BatchNo,PackageCode,PackageQty,Version,CreateBy,CreateDate,UDF12,UDF13,UDF14,UDF15,UDF16,UDF17,UDF18,DUDF01,DUDF02,DUDF03,DUDF04,DUDF05,DUDF08,DUDF09,DUDF10,DUDF11)
        VALUES(%(SkuStatus)s,%(LocationId)s,%(BillId)s,%(OrderLineNo)s,%(StorerId)s,%(SkuId)s,%(QtyPlan)s,%(BatchNo)s,%(PackageCode)s,%(PackageQty)s,%(Version)s,%(CreateBy)s,%(CreateDate)s,%(UDF12)s,%(UDF13)s,%(UDF14)s,%(UDF15)s,%(UDF16)s,%(UDF17)s,%(UDF18)s,%(DUDF01)s,%(DUDF02)s,%(DUDF03)s,%(DUDF04)s,%(DUDF05)s,%(DUDF08)s,%(DUDF09)s,%(DUDF10)s,%(DUDF11)s)
    '''

    CREATE_PICK_BILLID = '''
        DECLARE @Id VARCHAR(30) exec SP_GEN_ID 'SO',%s,'218',@Id OUTPUT SELECT @Id
    '''

    CREATE_ADJUSTNOTIFY_BILLID = '''
        DECLARE @Id VARCHAR(30) exec SP_GEN_COMMON_ID 'WAN',%s,'218','',@Id OUTPUT SELECT @Id
    '''

    GET_UNSEND_BILL = '''
        SELECT TOP 10 * FROM WRM_Inventory A 
        WHERE A.Status IN('50') AND NOT EXISTS(SELECT 1 FROM SYS_Order_Sync_Status WHERE BillId=A.BillId)
    '''

    GET_SEND_MESSAGE = '''
        SELECT A.BillId,C.FlowNo,A.OrderDate,A.WarehouseId,C.StorerId,C.UDF01,C.UDF02,C.UDF03, C.UDF04,C.UDF05,
        C.SkuId,C.BatchNo,C.LocationId,C.CID,C.Qty,D.WHAreaId,D.Property5,D.Property4 KCDD FROM 
        WRM_Inventory A INNER JOIN WRM_Scan B ON A.BillId=B.OrigBillId
        INNER JOIN WRM_ScanDetail C ON B.BillId=C.BillId
        INNER JOIN COM_Location D ON C.LocationId=D.LocationId
        WHERE A.BillId=''
    '''

    INSERT_ORDER_SYNC_STATUS = '''
        INSERT INTO dbo.SYS_Order_Sync_Status (OrderId,Status,OPT_By,OPT_Date,CreateBy,CreateDate,Memo)
        VALUES(%(OrderId)s,%(Status)s,%(OPT_By)s,%(OPT_Date)s,%(CreateBy)s,%(CreateDate)s,%(Memo)s)
    '''

    INSERT_MOVEIN_ORDER = '''
     IF NOT EXISTS (SELECT 1 FROM dbo.SRM_Order WHERE BillId = %(BillId)s)
    BEGIN
        INSERT INTO dbo.SRM_Order (BillId,StorerId,WarehouseId,InOutType,OrderType,SyncBillDate,Status,OrigSystem,GoodsCount,SkuCount,IsCharge,BatchNo,Ex1,Version,CreateBy,CreateDate)
        VALUES(%(BillId)s,%(StorerId)s,%(WarehouseId)s,%(InOutType)s,%(OrderType)s,%(SyncBillDate)s,%(Status)s,%(OrigSystem)s,%(GoodsCount)s,%(SkuCount)s,%(IsCharge)s,%(BatchNo)s,%(Ex1)s,%(Version)s,%(CreateBy)s,%(CreateDate)s)
    END
    '''

    INSERT_MOVEIN_ORDER_DETAIL = '''
        INSERT INTO dbo.SRM_OrderDetail (BillId,StorerId,SkuId,SkuStatus,QtyPlan,BatchNo,PackageCode,PackageQty,UDF01,UDF02,UDF03,UDF04,UDF05,Ex1,Version,CreateBy,CreateDate)
        VALUES(%(BillId)s,%(StorerId)s,%(SkuId)s,%(SkuStatus)s,%(QtyPlan)s,%(BatchNo)s,%(PackageCode)s,%(PackageQty)s,%(UDF01)s,%(UDF02)s,%(UDF03)s,%(UDF04)s,%(UDF05)s,%(CID)s,%(Version)s,%(CreateBy)s,%(CreateDate)s)
    '''

    INSERT_MOVEIN_SCAN = '''
         INSERT INTO dbo.SRM_Scan (BillId,OrigBillType,OrigBillId,SyncBillId,OrderType,StorerId,WarehouseId,OrderDate,Status,ScanType,Version,CreateBy,CreateDate,UDF01,UDF02,UDF03,UDF04,UDF05)
        VALUES(%(BillId_Scan)s,%(OrigBillType_Scan)s,%(BillId)s,%(SyncBillId)s,%(OrderType)s,%(StorerId)s,%(WarehouseId)s,%(OrderDate)s,%(Status)s,%(ScanType)s,%(Version)s,%(CreateBy)s,%(CreateDate)s,%(UDF01)s,%(UDF02)s,%(UDF03)s,%(UDF04)s,%(UDF05)s)
    '''

    INSERT_MOVEIN_SCAN_DETAIL = '''
         INSERT INTO dbo.SRM_ScanDetail (BillId,StorerId,SkuId,SkuStatus,QtyPlan,QtyIn,BatchNo,PackageCode,PackageQty,Version,CreateBy,CreateDate,UDF01,UDF02,UDF03,UDF04,UDF05)
        VALUES(%(BillId)s,%(StorerId)s,%(SkuId)s,%(SkuStatus)s,%(QtyPlan)s,%(QtyPlan)s,%(BatchNo)s,%(PackageCode)s,%(PackageQty)s,%(Version)s,%(CreateBy)s,%(CreateDate)s,%(UDF01)s,%(UDF02)s,%(UDF03)s,%(UDF04)s,%(UDF05)s)
    '''

    CREATE_REPLEN_BILLID = '''
        DECLARE @Id VARCHAR(30) exec SP_GEN_ID 'ASN',%s,'218',@Id OUTPUT SELECT @Id
    '''

    CREATE_MOVEIN_BILLID = '''
            DECLARE @Id VARCHAR(30) exec SP_GEN_ID 'ASN',%s,'218',@Id OUTPUT SELECT @Id
        '''

    CREATE_MOVEOUT_BILLID = '''
        DECLARE @Id VARCHAR(30) exec SP_GEN_ID 'PO',%s,'218',@Id OUTPUT SELECT @Id
    '''

    CREATE_SCAN_BILLID = '''
        DECLARE @Id VARCHAR(30) exec SP_GEN_COMMON_ID 'SCAN',%s,'218','',@Id OUTPUT SELECT @Id
    '''

    INSERT_MOVEOUT_ORDER = '''
        IF NOT EXISTS (SELECT 1 FROM dbo.SOM_Order WHERE BillId = %(BillId)s)
    BEGIN
        INSERT INTO dbo.SOM_Order (BusinessType,OrderSource,SOPType,BillId,StorerId,WarehouseId,OrderType,Status,OrigSystem,Version,CreateBy,CreateDate)
        VALUES(%(BusinessType)s,%(OrderSource)s,%(SOPType)s,%(BillId)s,%(StorerId)s,%(WarehouseId)s,%(OrderType)s,%(Status)s,%(OrigSystem)s,%(Version)s,%(CreateBy)s,%(CreateDate)s)
    END
    '''

    INSERT_MOVEOUT_SYNC_ORDER = '''
        INSERT INTO dbo.SOM_SyncOrder (BillId,SyncBillId,WarehouseId,StorerId,GoodsCount,SkuCount)
        VALUES(%(BillId)s,%(SyncBillId)s,%(WarehouseId)s,%(StorerId)s,%(GoodsCount)s,%(SkuCount)s)
    '''

    INSERT_MOVEOUT_ORDER_DETAIL = '''
        INSERT INTO dbo.SOM_OrderDetail (BillId,StorerId,SkuId,SkuStatus,Qty,Unit,Status,BatchNo,PackageCode,PackageQty,UDF01,UDF02,UDF03,UDF04,UDF05,Version,CreateBy,CreateDate)
        VALUES(%(BillId)s,%(StorerId)s,%(SkuId)s,%(SkuStatus)s,%(Qty)s,%(Unit)s,%(Status)s,%(BatchNo)s,%(PackageCode)s,%(PackageQty)s,%(UDF01)s,%(UDF02)s,%(UDF03)s,%(UDF04)s,%(UDF05)s,%(Version)s,%(CreateBy)s,%(CreateDate)s)
    '''

    INSERT_ORDER_TASK_DETAIL = '''
        INSERT INTO dbo.TRM_OrderTaskDetail (OrderId,StorerId,WarehouseId,FromLoc,BatchNo,SkuId,SkuStatus,QtyScan)
        VALUES(%(BillId)s,%(StorerId)s,%(WarehouseId)s,%(FromLoc)s,%(BatchNo)s,%(SkuId)s,%(SkuStatus)s,%(Qty)s)
    '''

    SELECT_UNSEND_MOVEIN_ORDER = '''
        SELECT TOP 10 * FROM SRM_Order A 
        WHERE A.Status IN('55') AND NOT EXISTS(SELECT 1 FROM SYS_Order_Sync_Status WHERE OrderId=A.BillId) AND A.OrderType IN('99')
    '''

    SELECT_UNSEND_MOVEIN_ORDER_DETAIL = '''
        SELECT A.SourceBillId,A.WarehouseId,A.StorerId,B.UDF01,C.Property4 KCDD,B.SkuId,B.BatchNo,B.UDF03,B.UDF04,B.UDF02,
        E.Ex9,E.Ex10,B.FromCID,D.Property5,C.WHAreaId ToWHAreaId,B.ToLoc,B.ToCID,B.QtyPlan,B.UDF05,A.CreateBy
        FROM TRM_TaskSJ A INNER JOIN TRM_TaskSJDetail B ON A.TaskId=B.TaskId
        INNER JOIN COM_Location C ON B.ToLoc=C.LocationId
        INNER JOIN COM_WHArea D ON C.WHAreaId=D.WHAreaId
        INNER JOIN SRM_Order E ON A.SourceBillId=E.BillId
        WHERE A.SourceBillId=%s
    '''

    SELECT_UNSEND_MOVEOUT_ORDER = '''
        SELECT TOP 10 * FROM SOM_Order A 
        WHERE A.Status IN('55') AND NOT EXISTS(SELECT 1 FROM SYS_Order_Sync_Status WHERE OrderId=A.BillId) AND A.OrderType IN('99')
    '''

    SELECT_UNSEND_MOVEOUT_ORDER_DETAIL = '''
        SELECT A.SourceBillId,A.WarehouseId,A.StorerId,C.Property4 KCDD,B.SkuId,B.BatchNo,B.UDF02,B.UDF03,B.UDF04,B.UDF05,
        D.Property5,A.WHAreaId FromWHAreaId,A.FromLoc,B.FromCID,E.Ex9,E.Ex10,B.ToCID,B.QtyPlan,F.CreateBy
        FROM TRM_TaskXJ A INNER JOIN TRM_TaskXJDetail B ON A.TaskId=B.TaskId
        INNER JOIN COM_Location C ON B.FromLoc=C.LocationId
        INNER JOIN COM_WHArea D ON D.WHAreaId=C.WHAreaId
        INNER JOIN SOM_SyncOrder E ON A.SourceBillId=E.BillId
        INNER JOIN SOM_Issue F ON E.BillId=F.OrigBillId
        WHERE A.SourceBillId=%s
    '''

    SELECT_UNSEND_MOVESAME_ORDER = '''
        SELECT TOP 10 * FROM WRM_MoveLoc A 
        WHERE A.Status IN('40') AND NOT EXISTS(SELECT 1 FROM SYS_Order_Sync_Status WHERE BillId=A.BillId)
    '''

    SELECT_UNSEND_MOVESAME_ORDER_DETAIL = '''
        SELECT A.BillId,A.WarehouseId,A.StorerId,C.Property4 KCDD,B.SkuId,B.FromBatchNo BatchNo,B.UDF02,B.UDF03,B.UDF04,B.UDF05,
        B.FromWHAreaId,B.FromLoc,B.FromCID,B.ToWHAreaId,B.ToLoc,B.ToCID,B.ToQty,A.ChargeBy
        FROM WRM_MoveLoc A INNER JOIN WRM_MoveLocDetail B ON A.BillId=B.BillId
        INNER JOIN COM_Location C ON B.FromLoc=C.LocationId
        WHERE A.BillId=%s
    '''

    SELECT_UNSEND_MOVEDIFFER_ORDER = '''
        SELECT TOP 10 * FROM SRM_Order A 
        WHERE A.Status IN('55') AND NOT EXISTS(SELECT 1 FROM SYS_Order_Sync_Status WHERE OrderId=A.BillId) AND A.OrderType IN('90')
    '''

    SELECT_UNSEND_MOVEDIFFER_ORDER_DETAIL = '''
        SELECT A.SourceBillId,A.WarehouseId,A.StorerId,C.Property4 KCDD,B.SkuId,B.BatchNo,B.UDF03,B.UDF04,B.UDF02,
        E.Ex9,E.Ex10,B.FromCID,D.Property5,C.WHAreaId ToWHAreaId,B.ToLoc,B.ToCID,B.QtyPlan,B.UDF05,A.CreateBy
        FROM TRM_TaskSJ A INNER JOIN TRM_TaskSJDetail B ON A.TaskId=B.TaskId
        INNER JOIN COM_Location C ON B.ToLoc=C.LocationId
        INNER JOIN COM_WHArea D ON C.WHAreaId=D.WHAreaId
        INNER JOIN SRM_Order E ON A.SourceBillId=E.BillId
        WHERE A.SourceBillId=%s 
    '''

    SELECT_UNSEND_LOCATION = '''
        SELECT LocationId,Property1,Property2,Property3,Property4,Property5 FROM COM_Location 
        WHERE WHAreaId IN(SELECT WHAreaId FROM COM_WHArea WHERE WHAreaType='PRODUCT')
    '''

    HANDLE_INSERT_REPLEN_ORDER =f'''
            BEGIN TRANSACTION
        DECLARE @issuccess int,@errmsg VARCHAR(100)
        SET @issuccess=1
        SET @errmsg = 'success'
            {INSERT_REPLEN_ORDER}
        IF @@ERROR=0
        BEGIN
            {INSERT_REPLEN_ORDER_DETAIL}
        END
        IF @@ERROR<>0
        BEGIN
            SET @issuccess = 0
            SET @errmsg = 'Insert Order ERROR!'
        END
        if @issuccess = 0
        BEGIN
            ROLLBACK TRANSACTION
            SELECT @issuccess as issuccess,@errmsg as errmsg
            RETURN
        END
        else
        BEGIN
            COMMIT TRANSACTION
            SELECT @issuccess as issuccess,@errmsg as errmsg
            RETURN
        END
    '''

    HANDLE_INSERT_REPLEN_ORDER1 = f'''
            BEGIN
            DECLARE @issuccess int,@errmsg VARCHAR(100)
            SET @issuccess=1
            SET @errmsg = 'success'
                {INSERT_REPLEN_ORDER}
            IF @@ERROR=0
            BEGIN
                {INSERT_REPLEN_ORDER_DETAIL}
            END
            IF @@ERROR<>0
            BEGIN
                SET @issuccess = 0
                SET @errmsg = 'Insert Order ERROR!'
            END
                SELECT @issuccess as issuccess,@errmsg as errmsg
                RETURN
            END
        '''

    HANDLE_INSERT_PICK_ORDER = f'''
        IF NOT EXISTS (SELECT 1 FROM dbo.SRM_Order WHERE SyncBillId = %(SyncBillId)s)
            BEGIN
            DECLARE @issuccess int,@errmsg VARCHAR(100)
            SET @issuccess=1
            SET @errmsg = 'success'
                {INSERT_PICK_ORDER}
            IF @@ERROR=0
            BEGIN
                {INSERT_PICK_ORDER_DETAIL}
            END
            IF @@ERROR=0
            BEGIN
                {INSERT_PICK_SYNC_ORDER}
            END
            IF @@ERROR<>0
            BEGIN
                SET @issuccess = 0
                SET @errmsg = 'Insert Order ERROR!'
            END
                SELECT @issuccess as issuccess,@errmsg as errmsg
                RETURN
            END
        '''

    HANDLE_INSERT_PICK_ORDER1 = f'''
            BEGIN
            DECLARE @issuccess int,@errmsg VARCHAR(100)
            SET @issuccess=1
            SET @errmsg = 'success'
                {INSERT_PICK_ORDER}
                {INSERT_PICK_ORDER_DETAIL}
                {INSERT_PICK_SYNC_ORDER}
            IF @@ERROR<>0
            BEGIN
                SET @issuccess = 0
                SET @errmsg = 'Insert Order ERROR!'
            END
                SELECT @issuccess as issuccess,@errmsg as errmsg
                RETURN
            END
            '''

    HANDLE_INSERT_ADJUST_NOTIFY_ORDER = f'''
                BEGIN
            DECLARE @issuccess int,@errmsg VARCHAR(100)
            SET @issuccess=1
            SET @errmsg = 'success'
                {INSERT_ADJUSTNOTIFY}
                {INSERT_ADJUSTNOTIFY_DETAIL}
            IF @@ERROR<>0
            BEGIN
                SET @issuccess = 0
                SET @errmsg = 'Insert Order ERROR!'
            END
                SELECT @issuccess as issuccess,@errmsg as errmsg
                RETURN
            END
        '''

    HANDLE_INSERT_SKU = f'''
                    BEGIN
                DECLARE @issuccess int,@errmsg VARCHAR(100)
                SET @issuccess=1
                SET @errmsg = 'success'
                    {SKU_UPSERT}
                    {SKUUPC_UPSERT}
                    {STORER_UPSERT}
                IF @@ERROR<>0
                BEGIN
                    SET @issuccess = 0
                    SET @errmsg = 'Insert Order ERROR!'
                END
                    SELECT @issuccess as issuccess,@errmsg as errmsg
                    RETURN
                END
            '''

    HANDLE_INSERT_POST_REPLEN_ORDER = f'''
        BEGIN
                DECLARE @issuccess int,@errmsg VARCHAR(100)
                SET @issuccess=1
                SET @errmsg = 'success'
                    {UPDATE_RECEIPT_DETAIL}
                    {RECEIPT_QMUPDATE}
                    {INSERT_ORDER_SYNC_STATUS}
                IF @@ERROR<>0
                BEGIN
                    SET @issuccess = 0
                    SET @errmsg = 'Insert Order ERROR!'
                END
                    SELECT @issuccess as issuccess,@errmsg as errmsg
                    RETURN
                END
    '''

    IS_EXIST_REPLEN_ORDER = '''
        SELECT 1 FROM dbo.SRM_Order WHERE SyncBillId = %s AND Status not in ('00','55')
    '''

    IS_EXIST_PICK_ORDER = '''
        SELECT 1 FROM dbo.SOM_Order WHERE SyncBillId = %s AND Status not in ('00','55')
    '''

def PICK_ORDER(pick_order,syncbillid):
    res = f'''
            IF NOT EXISTS (SELECT 1 FROM dbo.SOM_Order WHERE SyncBillId = \'{syncbillid}\' AND Status not in ('00','55'))
            BEGIN
            DECLARE @issuccess int,@errmsg VARCHAR(100)
            SET @issuccess=1
            SET @errmsg = 'success'
                {pick_order}
            IF @@ERROR<>0
            BEGIN
                SET @issuccess = 0
                SET @errmsg = 'Insert Order ERROR!'
            END
                SELECT @issuccess as issuccess,@errmsg as errmsg
                RETURN
            END
    '''
    return res

def REPLEN_ORDER(replen_order,syncbillid):
    res = f'''
            IF NOT EXISTS (SELECT 1 FROM dbo.SRM_Order WHERE SyncBillId = \'{syncbillid}\' AND Status not in ('00','55'))
            BEGIN
            DECLARE @issuccess int,@errmsg VARCHAR(100)
            SET @issuccess=1
            SET @errmsg = 'success'
                {replen_order}
            IF @@ERROR<>0
            BEGIN
                SET @issuccess = 0
                SET @errmsg = 'Insert Order ERROR!'
            END
                SELECT @issuccess as issuccess,@errmsg as errmsg
                RETURN
            END
    '''
    return res

def BATCH_MODIFICATION(batch_modification,batch_no):
    res = f'''
            BEGIN
            DECLARE @issuccess int,@errmsg VARCHAR(100)
            SET @issuccess=1
            SET @errmsg = 'success'
                {batch_modification}
            IF @@ERROR<>0
            BEGIN
                SET @issuccess = 0
                SET @errmsg = 'Insert Order ERROR!'
            END
                SELECT @issuccess as issuccess,@errmsg as errmsg
                RETURN
            END
    '''
    return res