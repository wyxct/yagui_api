
 //操作栏的格式化
function addFunctionAlty1(value, row, index) {
	
	return [
	'<button id="pause" type="button" class="btn btn-default">暂停</button> &nbsp;&nbsp;'
	].join("");
}

function addFunctionAlty2(value, row, index) {

	return [
	'<button id="resume" type="button" class="btn btn-default">恢复</button> &nbsp;&nbsp;'
	].join("");
}
function addFunctionAlty0(value, row, index) {

	return [
	'<button id="start" type="button" class="btn btn-default">开始</button> &nbsp;&nbsp;'
	].join("");
}

function addFunctionAlty3(value, row, index) {

	return [
	'<button id="update" type="button" class="btn btn-default">更新</button> &nbsp;&nbsp;'
	].join("");
}

window.operateEvents = {
    'click #pause': function (e, vlaue, row, index) {
		pasuseone(row["name"])
    },
    'click #resume':function(e,vlaue,row,index)
	{
		resumeone(row["name"])
	},
    'click #start':function(e,vlaue,row,index)
	{
		addtask(row["name"])
	},
    'click #update':function(e,vlaue,row,index)
	{
        console.log("更新");
		updatetask(row)
	}
};

function updatetask(job) {
    $("#tx_task_no").val(job["name"]);
    $("#tx_ptr").val(job["trigger_time"]);
    $('#qtyModal').modal();
    
    
}

function updateptr() {
   ptr = $('#tx_ptr').val(),
   task_no = $('#tx_task_no').val(),
   $.ajax({
    type: 'PUT',
    url: 'api/tasks/'+task_no+'/',
    contentType:'application/json',
    dataType:'json',
    async: false,
    data:JSON.stringify({"cron" :ptr}),
    success: function(data){
        location.reload();
    },
    error: function(data){
      console.log(data.responseJSON["error"]);
      alert("错误："+data.responseJSON["error"]  )
    // location.reload()
    }
    }) 
}

function resumeone(jobname) {
    $.ajax({
    type: 'POST',
    url: 'api/tasks/'+jobname+'/resume/',
    contentType:'application/json',
    dataType:'json',
    async: false,
    data:JSON.stringify({"cron" :"0/8 * * * * * *"}),
    success: function(data){
        location.reload();
    },
    error: function(data){
      console.log(data.responseJSON["error"]);
      alert("错误："+data.responseJSON["error"]  )
    // location.reload()
    }
    })
}


function addtask(name) {
    
    //jobname = $('#taskid').val();
    jobname = name
    $.ajax({
    type: 'POST',
    url: 'api/tasks/'+jobname+'/start/',
    contentType:'application/json',
    dataType:'json',
    async: false,
    data:JSON.stringify({"cron" :"0/8 * * * * * *"}),
    success: function(data){
        location.reload();
    },
    error: function(data){
      console.log(data.responseJSON["error"]);
      alert("错误："+data.responseJSON["error"]  )
    // location.reload()
    }
    })
}
function pasuseone(jobname) {
    $.ajax({
    type: 'POST',
    url: 'api/tasks/'+jobname+'/pause/',
    contentType:'application/json',
    dataType:'json',
    async: false,
    data:JSON.stringify({"cron" :"0/8 * * * * * *"}),
    success: function(data){
        location.reload();
    },
    error: function(data){
      console.log(data.responseJSON["error"]);
      alert("错误："+data.responseJSON["error"]  )
    // location.reload()
    }
    })
}

function reloadtask() {
    $.ajax({
    type: 'POST',
    url: 'api/tasks/reload/',
    contentType:'application/json',
    dataType:'json',
    async: false,
    data:JSON.stringify({"cron" :"0/8 * * * * * *"}),
    success: function(data){
        location.reload();
    },
    error: function(data){
      console.log(data.responseJSON["error"]);
      alert("错误："+data.responseJSON["error"]  )
    // location.reload()
    }
    })
}

 var InitTable = function (url) {
     //先销毁表格
      $('#table').bootstrapTable("destroy");
      //加载表格
      $('#table').bootstrapTable({
          rowStyle: function (row, index) {//row 表示行数据，object,index为行索引，从0开始
              var style = "";
              if (row.SignInTime == '' || row.SignOutTime=='') {
                 style = { css: { 'color': 'red' } };
             }
             return  style;
         },
        searchAlign: 'left',
        search: true,   //显示隐藏搜索框
         showHeader: true,     //是否显示列头
         //classes: 'table-no-bordered',
         showLoading: true,
        undefinedText: '',
         showFullscreen: false,
         toolbarAlign: 'left',
         paginationHAlign: 'right',
         silent: true,
         url: url,
         method: 'get',                      //请求方式（*）
		 contentType:'application/json',
		 dataType:'json',
         toolbar: '#toolbar',                //工具按钮用哪个容器
         striped: true,                      //是否显示行间隔色
         cache: false,                       //是否使用缓存，默认为true，所以一般情况下需要设置一下这个属性（*）
         pagination: true,                   //是否显示分页（*）
         sortable: false,                     //是否启用排序
         sortOrder: "asc",                   //排序方式
         queryParamsType:'',//设置请求参数格式
		queryParams:function queryParams(params) {   //设自定义查询参数
			var param = {
				"offset": 0, "limit": 'all'
			};
			return param;
		},
        /*
		responseHandler:function(res) {
			console.log(res);
			console.log(res.data);
			//console.log(res.data.length);
			var param = {
				total: res.data.length,
				rows: res.data

			};
			return param;
		},*/
		locale:'zh-CN',
         sidePagination: "client",           //分页方式：client客户端分页，server服务端分页（*）
         pageNumber: 1,                       //初始化加载第一页，默认第一页
         pageSize: 10,                       //每页的记录行数（*）
         pageList: [2, 5, 10, 15],        //可供选择的每页的行数（*）
         search: true,                      //是否显示表格搜索，此搜索是客户端搜索，不会进服务端，所以，个人感觉意义不大
         strictSearch: false,
         //showColumns: true,                  //是否显示所有的列
         //showRefresh: true,                  //是否显示刷新按钮
         minimumCountColumns: 2,             //最少允许的列数
         clickToSelect: true,                //是否启用点击选中行
         //height: 680,                        //行高，如果没有设置height属性，表格自动根据记录条数觉得表格高度
         uniqueId: "ID",                     //每一行的唯一标识，一般为主键列
         //showToggle: true,                    //是否显示详细视图和列表视图的切换按钮
         //cardView: false,                    //是否显示详细视图
         detailView: false,                   //是否显示父子表
         //showExport: true,
		//	exportDataType: 'all',
         exportDataType: "selected",        //导出checkbox选中的行数
         paginationLoop: false,             //是否无限循环
         columns: [
        {
                 field: 'name',
                 title: '任务编号'
         }, {
                 field: 'trigger',
                 title: '触发方式'
         },
         {
                 field: 'trigger_time',
                 title: '触发参数'
         },
        {
                 field: 'desc',
                 title: '描述'
         },
        //{
        //         field: 'start_date',
        //        title: '开始时间'
        //},
         {
                 field: 'next_run_time',
                 title: '下次执行时间'
         }, {
                 field: 'state',
                 title: '状态'
         },
         {
                field: 'operate',
                title : '开始',
                events:operateEvents,
                formatter : addFunctionAlty0
         },
         {
                field: 'operate1',
                title : '暂停',
                events:operateEvents,
                formatter : addFunctionAlty1
         },{
                field: 'operate2',
                title : '恢复',
                events:operateEvents,
                formatter : addFunctionAlty2
         },
         {
                field: 'operate3',
                title : '更新',
                events:operateEvents,
                formatter : addFunctionAlty3
         },],
		  onLoadSuccess: function (data) {
			   console.log(data)
			 //window.parent.refleshBootStrapTable();		 
                },
		onLoadError: function (data) {
			alert("数据加载失败或当前无异常数据！");
		}
     });
     return InitTable;
 };
 

 InitTable("/api/tasks/");



/*-------------------insert/delete row---------------------*/