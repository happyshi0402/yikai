/**
 * Created by lsl on 2015/5/27.
 /**/
;(function($){
    $.fn.extend({
        /*可自定制
         * fields支持三种类型：
         * 1、‘’：data.data中直接存放显示值;
         * 2、‘a’单字段：显示字段与实际传输字段相同，都为a
         * 3、'a b'双字段,以空格分离,显示字段为a,实际传输字段为b
         * 4、‘callback’为回调函数字符串
         eg:
         //样本类型
         //move 移动样本
         $('#move_award_project').GlFilterTipInput({
         'url':'/sample/get/project/',
         'fields':'project_name project_no',
         'type':'move_sample',
         'ul_ID':'move_award_project_ul',
         'callback':"move()"
         });
         */
        'GlFilterTipInput':function(options){

            function changeUl(input) {//savedValue 为实际需要的值
                console.log('GlFilterTipInput options:',options);
                var fields=options.fields.split(" ");
                var field0=fields[0];
                if(fields.length==2)
                    var field1=fields[1];
                //console.log("fields",fields);
                $.ajax({
                    url:options.url,
                    type:'POST',
                    data:{q:input.value.replace(/(^\s*)|(\s*$)/g,'')},
                    success:function(data){
                        console.log("GLFilterTip returned data:",data);
                        if(data.success){
                            var result=data.data;
                            $("#"+options.ul_ID).empty();
                            if(field0=='')
                                for(var i=0;i<result.length;i++){
                                    $("<li id='"+input.id+"_ul_li"+i+"' savedValue='"+result[i]+"'>"+result[i]+"</li>").appendTo($("#"+options.ul_ID));
                                }
                            else
                                for(var i=0;i<result.length;i++){
                                    $("<li id='"+input.id+"_ul_li"+i+"' savedValue='"+result[i][field1]+"'>"+result[i][field0]+"</li>").appendTo($("#"+options.ul_ID));
                                }
                            //新建病号
                            if(options.type=="new_patient"){
                                if(input.value)
                                    $("<li id='"+input.id+"_ul_li_new'>新建病案号："+input.value+"</li>").appendTo($("#"+options.ul_ID));
                            }
                            if($("#"+options.ul_ID+' li').length)
                                $("#"+options.ul_ID).show();
                            else
                                $("#"+options.ul_ID).hide();
                        }else{
                            if(data.message)
                                swal(data.message);
                            else
                                swal("获取数据失败！");
                            $("#"+options.ul_ID).hide();
                        }
                    },
                    error:function(){
                        swal("网络请求失败！","请刷新后重试","error");
                        $("#"+options.ul_ID).hide();
                    }
                });
            }
            function inputClickHandler() {
                changeUl(this);
            }
            function inputKeyUpHandler(event) {
                //输入为空
                if (this.value == "") {
                    changeUl(this);
                }else {//输入不为空
                    if (!($("#"+options.ul_ID).css("display") != "none" && (event.keyCode == 38 || event.keyCode == 40 || event.keyCode == 13))) {
                        changeUl(this);
                    }
                }
            }
            function ulClickHandler(event) {
                //阻止事件冒泡
                var ev = event || window.event;
                if(ev.stopPropagation){
                    ev.stopPropagation();
                }else if(window.event){
                    window.event.cancelBubble = true;//兼容IE
                }

                if (options.type == 'new_patient' && event.target.getAttribute("id").split("li_")[1] == "new") {
                    event.data.$input.attr("savedValue",'');
                } else{
                    switch(navigator.appCodeName)
                    {
                        case "Mozilla"://IE  Firefox
                        {
                            event.data.$input.val(event.target.textContent);
                            break;
                        }
                        default:
                        {//360？
                            event.data.$input.val(event.target.innerText);
                            break;
                        }
                    }
                    event.data.$input.attr("savedValue",event.target.getAttribute('savedValue'));
                }
                $("#"+options.ul_ID).hide();
                //触发回调函数
                eval(options.callback);
            }


            this.bind('click',inputClickHandler);
            this.bind('keyup',inputKeyUpHandler);
            $('#'+options.ul_ID).bind('click',{'$input':this},ulClickHandler);

            //这个地方还是存在隐患的,不够友好
            var $others = $("body *").not("#"+options.ul_ID);
            $others.bind('click',function(){
                //console.log('GlFilterTipInput hide');
                $("#"+options.ul_ID).hide();
            });

            return this;
        },

        /*
         *前端常规提示
         默认 input savedValue属性中保存最终需要的数据
         * 1、displayField显示字段;//li显示字段  必需
         * 2、valueField实际传值字段//li传值字段  非必需
         * 3、dataType 数据格式 text json  必需
         * 4、ul_ID  必需
         * 5、'maxNum':20(默认), 非必需
         * 6、‘callBack'回调函数  非必需
         */
        'FrontCommonTipInput':function(options){

            function getData(){
                $.ajax({
                    url:options.url,
                    type:'GET',
                    dataType:options.dataType,
                    success:function(result){
                        console.log("FrontCommonTipInput returned data:",result);
                        switch (options.dataType) {
                            case 'text':
                            {
                                options.getAll=true;
                                var geneNameArray=result.split('\n');
                                for(var i in geneNameArray){
                                    var item={'defaultField':geneNameArray[i]};
                                    options.displayField='defaultField';
                                    allItems.push(item);
                                }
                                //console.log('allItems:',allItems);
                                filterData(document.getElementById(options.id).value);
                                changeUl(document.getElementById(options.id));
                                break;
                            }
                            case 'json':
                            {
                                if(result.success){
                                    options.getAll=true;
                                    allItems=result.data;
                                    //console.log('allItems:',allItems);
                                    filterData(document.getElementById(options.id).value);
                                    changeUl(document.getElementById(options.id));
                                }else{
                                    if(result.message)
                                        swal(result.message);
                                    else
                                        swal("获取数据失败！");
                                }
                                break;
                            }
                        }
                    },
                    error:function(){
                        swal("FrontCommonTipInput "+options.url+" 网络请求失败！","请刷新后重试","error");
                    }
                });
            }
            function selectAndSortArray(array,field){//对数组按照某个number型字段排序
                var sortedArray=[];
                for(var j in array){
                    if(!sortedArray.length){
                        sortedArray.push(array[j]);
                    }else{
                        for(var k=0;k<sortedArray.length;k++){
                            if(array[j][field]<=sortedArray[k][field]){
                                sortedArray.splice(k,0,array[j]);
                                break;
                            }
                        }
                        if(k==sortedArray.length){
                            sortedArray.push(array[j]);
                        }
                    }
                }
                //console.log('sortedArray',sortedArray);
                return sortedArray;
            }
            function filterData(text){
                //console.log('text:',text);
                if(text!=''){
                    var tempItems=[];
                    for(var i in allItems) {
                        var index = allItems[i][options.displayField].toUpperCase().indexOf(text.toUpperCase());
                        if (index != -1) {
                            allItems[i].searchedIndex = index;
                            tempItems.push(allItems[i]);
                        }
                        if(tempItems.length>=maxNum)
                            break;
                    }
                    currentItems=selectAndSortArray(tempItems,'searchedIndex');
                }else{
                    currentItems=allItems.slice(0,maxNum);//如果长度大于了数组长度 也不会报错
                }
                //console.log('FrontCommonTipInput filtered data:',currentItems);
            }
            function changeUl(input) {//savedValue 为实际需要的值
                //console.log(input.value);
                $("#"+options.ul_ID).empty();
                if(options.hasOwnProperty('valueField')){
                    for(var i=0;i<currentItems.length;i++){
                        $("<li id='"+input.id+"_ul_li"+i+"' savedValue='"+currentItems[i][options.valueField]+"'>"+currentItems[i][options.displayField]+"</li>").appendTo($("#"+options.ul_ID));
                    }
                }else{
                    for(var i=0;i<currentItems.length;i++){
                        $("<li id='"+input.id+"_ul_li"+i+"' savedValue='"+currentItems[i][options.displayField]+"'>"+currentItems[i][options.displayField]+"</li>").appendTo($("#"+options.ul_ID));
                    }
                }
                if(options.hasOwnProperty('ownType') && options['ownType']=="new_patient"){
                    if(input.value)
                        $("<li id='"+input.id+"_ul_li_new' savedValue='"+input.value+"'>新建病案号："+input.value+"</li>").appendTo($("#"+options.ul_ID));
                }
                //console.log($("#"+options.ul_ID).children().length);
                if($("#"+options.ul_ID).children().length){
                    console.log("show")
                    $('#'+options.ul_ID).show();
                }else{
                    console.log("hide")
                    $('#'+options.ul_ID).hide();
                }
            }
            function inputClickHandler(event){
                //console.log('FrontCommonTipInput options:',options);
                //阻止事件冒泡,这个地方和下边点击其他处隐藏有冲突需要处理
                var ev = event || window.event;
                if(ev.stopPropagation){
                    ev.stopPropagation();
                }else if(window.event){
                    window.event.cancelBubble = true;//兼容IE
                }

                if(!options.getAll){
                    getData();
                }else{
                    filterData(this.value);
                    changeUl(this);
                }
            }
            function inputKeyUpHandler(event) {
                //console.log('keyup');
                filterData(this.value);
                changeUl(this);
            }
            function ulClickHandler(event) {
                //阻止事件冒泡
                var ev = event || window.event;
                if(ev.stopPropagation){
                    ev.stopPropagation();
                }
                else if(window.event){
                    window.event.cancelBubble = true;//兼容IE
                }

                if (options.hasOwnProperty('ownType') && options['ownType']=="new_patient" && event.target.getAttribute("id").split("li_")[1] == "new") {
                    console.log('new_patient');
                } else {
                    //不同的浏览器竟然变量内部结构不一样，IE是event.target.innerText；火狐是event.target.textContent
                    // alert(navigator.appCodeName);
                    switch (navigator.appCodeName) {
                        case "Mozilla"://IE  Firefox
                        {
                            event.data.$input.val(event.target.textContent);
                            event.data.$input.attr("savedValue", event.target.getAttribute('savedValue'));
                            break;
                        }
                        default://360？
                            event.data.$input.val(event.target.innerText);
                            event.data.$input.attr("savedValue", event.target.getAttribute('savedValue'));
                    }
                }
                $("#"+options.ul_ID).hide();
                if(options.hasOwnProperty('callback'))
                    eval(options['callback']);
            }

            options['id']=this.attr('id');
            options.getAll=false;
            console.log('FrontCommonTipInput options:',options);
            var allItems=[];
            var currentItems=[];
            var maxNum=20;
            if(options.hasOwnProperty('maxNum'))
                maxNum=options['maxNum'];
            this.bind('click',inputClickHandler);
            this.bind('keyup',inputKeyUpHandler);
            $('#'+options.ul_ID).bind('click',{'$input':this},ulClickHandler);
            var $others = $("body *").not("#"+options.id).not("#"+options.ul_ID);
            $others.bind('click',ul_hide);
            function ul_hide(){
                console.log('FrontCommonTipInput hide');
                $("#"+options.ul_ID).hide();
            }
            //$("#"+options.id).unbind("click",ul_hide);
            return this;
        }
    });
})(jQuery);
