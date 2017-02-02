/*

C:\Users\Administrator\Desktop\000001.xls
http://query.sse.com.cn/marketdata/tradedata/queryTradingByProdTypeData.do?jsonCallBack=jsonpCallback84790&searchDate=2017-01-24&prodType=gp&_=1485792516678

*/
	//日股票情况
	if($stockday.length>0){
	
		var day = get_lastTradeDate_global();
		//$("#start_date2").val(day);
		
		
		function showajaxStockday(){
			showloading();
			$.ajax({
				url:sseQueryURL+'marketdata/tradedata/queryTradingByProdTypeData.do',
				type:'post',
				async:false,
				cache : false,
				dataType: "jsonp",
				jsonp: "jsonCallBack",
				jsonpCallback: "jsonpCallback" + Math.floor(Math.random() * (100000 + 1)),
				data: {
					searchDate:day,
					prodType:'gp'
				},  
				async:false,
				cache : false,
				success:function(data){
						var item = data.result;
						var header = [
										["","<div class='th_div_center'>单日情况</div>"],
										["","<div class='th_div_center'>上海市场</div>"],
										["","<div class='th_div_center'>A股</div>"],
										["","<div class='th_div_center'>B股</div>"]
									];
							var tempArr = [];
							var headerlength = header.length;
							tempArr.push("<tr>");
							for (var j = 0; j < header.length; ++j){
								tempArr.push("<th>"+header[j][1]+"</th>");
							}
							tempArr.push("</tr>");
						
						if(item[0].marketValue==""){
							tempArr.push("<tr><td colspan='50'>没有数据！</td></tr>");
							$(".sse_table_title2").hide();
						}else{
						
							var list = [
										['市价总值(亿元)', '<div class="align_right">'+item[2].marketValue+'</div>' ,'<div class="align_right">'+item[0].marketValue+'</div>' ,'<div class="align_right">'+item[1].marketValue+'</div>'],	
										['流通市值(亿元)','<div class="align_right">'+ item[2].negotiableValue+'</div>', '<div class="align_right">'+item[0].negotiableValue+'</div>','<div class="align_right">'+item[1].negotiableValue+'</div>'],	
										['成交量(万股)', '<div class="align_right">'+item[2].trdVol+'</div>', '<div class="align_right">'+item[0].trdVol+'</div>','<div class="align_right">'+item[1].trdVol+'</div>'],	
										['成交金额(亿元)', '<div class="align_right">'+item[2].trdAmt+'</div>', '<div class="align_right">'+item[0].trdAmt+'</div>','<div class="align_right">'+item[1].trdAmt+'</div>'],	
										['成交笔数(万笔)','<div class="align_right">'+ item[2].trdTm+'</div>', '<div class="align_right">'+item[0].trdTm+'</div>','<div class="align_right">'+item[1].trdTm+'</div>'],	
										['平均市盈率', '<div class="align_right">'+item[2].profitRate+'</div>', '<div class="align_right">'+item[0].profitRate+'</div>','<div class="align_right">'+item[1].profitRate+'</div>'],
										['换手率(%)','<div class="align_right">'+ifundefindTurn(item[2].exchangeRate)+'</div>','<div class="align_right">'+ifundefindTurn(item[0].exchangeRate)+'</div>','<div class="align_right">'+ifundefindTurn(item[1].exchangeRate)+'</div>']
										];
								//创建表格内容
								var listLen = list.length;
								for (var k = 0; k < listLen; ++k){
									var items = list[k];
									tempArr.push("<tr>");
									for (var l = 0; l < items.length; ++l){
										var item = items[l]
										tempArr.push("<td>"+item+"</td>");
									}
									tempArr.push("</tr>");
								}
								
							}
								$(".sse_table_title2").show();
								$(".sse_table_title2").find("p").html('数据日期：'+day);
								$('.js_tableT01').find('.table').html(tempArr.join(""));
								//$('.sse_table_conment').show().find('p').html('*本日的数据统计至前1交易日');
								
						},
						complete:function(){
							hideloading();
						}
				});  
				
		} 