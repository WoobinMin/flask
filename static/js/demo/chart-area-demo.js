// Set new default font family and font color to mimic Bootstrap's default styling
Chart.defaults.global.defaultFontFamily = 'Nunito', '-apple-system,system-ui,BlinkMacSystemFont,"Segoe UI",Roboto,"Helvetica Neue",Arial,sans-serif';
Chart.defaults.global.defaultFontColor = '#858796';

function number_format(number, decimals, dec_point, thousands_sep) {
  // *     example: number_format(1234.56, 2, ',', ' ');
  // *     return: '1 234,56'
  number = (number + '').replace(',', '').replace(' ', '');
  var n = !isFinite(+number) ? 0 : +number,
    prec = !isFinite(+decimals) ? 0 : Math.abs(decimals),
    sep = (typeof thousands_sep === 'undefined') ? ',' : thousands_sep,
    dec = (typeof dec_point === 'undefined') ? '.' : dec_point,
    s = '',
    toFixedFix = function(n, prec) {
      var k = Math.pow(10, prec);
      return '' + Math.round(n * k) / k;
    };
  // Fix for IE parseFloat(0.55).toFixed(0) = 0;
  s = (prec ? toFixedFix(n, prec) : '' + Math.round(n)).split('.');
  if (s[0].length > 3) {
    s[0] = s[0].replace(/\B(?=(?:\d{3})+(?!\d))/g, sep);
  }
  if ((s[1] || '').length < prec) {
    s[1] = s[1] || '';
    s[1] += new Array(prec - s[1].length + 1).join('0');
  }
  return s.join(dec) + unit;
}

var jsonParsingDatas1 = {
  CamPosName: [],
  PlayTime: [],
  HookCount: [],
  UndoCount: [],
  RetryCount: [],
}

var jsonParsingDatas2 = {
  CamPosName: [],
  PlayTime: [],
  HookCount: [],
  UndoCount: [],
  RetryCount: [],
}

var unit = ""


var xhr1 = new XMLHttpRequest();
var jsonData = [];
xhr1.open("GET", "static/document/UserStageDatas_2023-08-26.json" , true)
xhr1.onreadystatechange = function() {
  if(xhr1.readyState == 4 && xhr1.status == 200)
  {
    jsonData.push(JSON.parse(xhr1.responseText));
    for (var i = 0; i < jsonData[0].length; i++) {
      jsonParsingDatas1.CamPosName.push(jsonData[0][i].CamPosName);
      jsonParsingDatas1.PlayTime.push(jsonData[0][i].PlayTime);
      jsonParsingDatas1.HookCount.push(jsonData[0][i].HookCount)
      jsonParsingDatas1.UndoCount.push(jsonData[0][i].UndoCount)
      jsonParsingDatas1.RetryCount.push(jsonData[0][i].RetryCount)
    }
  }
}
xhr1.send();

var xhr2 = new XMLHttpRequest();
xhr2.open("GET", "static/document/UserStageDatas_2023-08-27.json" , true)
xhr2.onreadystatechange = function() {
  if(xhr2.readyState == 4 && xhr2.status == 200)
  {
    jsonData.push(JSON.parse(xhr2.responseText));
    for (var i = 0; i < jsonData[1].length; i++) {
      jsonParsingDatas2.CamPosName.push(jsonData[1][i].CamPosName);
      jsonParsingDatas2.PlayTime.push(jsonData[1][i].PlayTime);
      jsonParsingDatas2.HookCount.push(jsonData[1][i].HookCount)
      jsonParsingDatas2.UndoCount.push(jsonData[1][i].UndoCount)
      jsonParsingDatas2.RetryCount.push(jsonData[1][i].RetryCount)
    }
  }

  // 기본으로 PlayTime을 보여줌
  SetPlayTimeGraph();
}
xhr2.send();

document.addEventListener("DOMContentLoaded", Init)

function Init()
{
  var checkBox1 = document.getElementById("day1CheckBox");
  var checkBox2 = document.getElementById("day2CheckBox");

  checkBox1.addEventListener("change", function(){
    console.log("checkbox1 changed : " + !checkBox1.checked);
    SetDataSetHidden(0, !checkBox1.checked);
    myLineChart.update();
  });

  checkBox2.addEventListener("change", function(){
    SetDataSetHidden(1, !checkBox2.checked);
    console.log("checkbox2 changed : " + !checkBox2.checked);
    myLineChart.update();
  });

}

//charData에 라벨추가
function AddLabel(label){
  chartData.labels.push(label);
}

//chartData에 dataset[datasetIndex]에 데이터 추가
function AddData(datasetIndex, data) {
  chartData.datasets[datasetIndex].data.push(data);
}

//chartdata에 할당된 data와 label 삭제
function RemoveAllData(){
  for(var i = 0; i < jsonData[0].length; i++)
  {
    chartData.labels.pop();
    chartData.datasets.forEach((dataset) => {
      dataset.data.pop();
    });
  }
}

// 표 좌측 단위 변경 및 마우스 올릴 시 나오는 popup데이터 표시 변경
function ChangeInfoes(datasetIndex, label, unit){
  chartData.datasets[datasetIndex].label  = label;
  this.unit = unit;
}

//chartData의 datasets[datasetIndex]가 숨겨질 지 설정
function SetDataSetHidden(datasetIndex, isHidden)
{
  chartData.datasets[datasetIndex].hidden = isHidden;
}

// jsonData[0]에 등록된 모든 Label을 chartData에 추가
function AddAllLabelToChartData()
{
  for(var i = 0; i < jsonData[0].length; i++)
    AddLabel(jsonParsingDatas1.CamPosName[i]);
}

// dayIndex날짜의 CheckBox의 값을 return
function GetCheckBoxValue(dayIndex)
{
  var checkBoxID = "";
  if(dayIndex == 0)
  {
    checkBoxID = "day1CheckBox";
  }
  else if(dayIndex == 1)
  {
    checkBoxID = "day2CheckBox";
  }
  else
    return false;

  var checkBox = document.getElementById(checkBoxID);
  if(checkBox == null) return false;

  return checkBox.checked;
}

document.getElementById('QADataPlayTime').onclick = SetPlayTimeGraph;
document.getElementById('QADataHookCount').onclick = SetHookCountGraph;
document.getElementById('QADataUndoCount').onclick = SetUndoCountGraph;
document.getElementById('QADataRetryCount').onclick = SetRetryCountGraph;

function SetPlayTimeGraph()
{
  RemoveAllData(myLineChart);
  AddAllLabelToChartData();

  for(var i = 0; i < jsonData[0].length; i++)
    AddData(0, jsonParsingDatas1.PlayTime[i]);

  for(var i = 0; i < jsonData[1].length; i++)
    AddData(1, jsonParsingDatas2.PlayTime[i]);

  SetDataSetHidden(0, !GetCheckBoxValue(0));
  SetDataSetHidden(1, !GetCheckBoxValue(1));
    
  ChangeInfoes(0,"Day1", "(s)");
  ChangeInfoes(1,"Day2", "(s)");
  myLineChart.update()
}

function SetHookCountGraph()
{
  RemoveAllData(myLineChart);
  AddAllLabelToChartData();

  for(var i = 0; i < jsonData[0].length; i++)
    AddData(0, jsonParsingDatas1.HookCount[i]);

  for(var i = 0; i < jsonData[1].length; i++)
    AddData(1, jsonParsingDatas2.HookCount[i]);

  SetDataSetHidden(0, !GetCheckBoxValue(0));
  SetDataSetHidden(1, !GetCheckBoxValue(1));
    
  ChangeInfoes(0,"Day1", "(times)");
  ChangeInfoes(1,"Day2", "(times)");
  myLineChart.update()
}

function SetUndoCountGraph()
{
  RemoveAllData(myLineChart);
  AddAllLabelToChartData();

  for(var i = 0; i < jsonData[0].length; i++)
    AddData(0, jsonParsingDatas1.UndoCount[i]);

  for(var i = 0; i < jsonData[1].length; i++)
    AddData(1, jsonParsingDatas2.UndoCount[i]);

  SetDataSetHidden(0, !GetCheckBoxValue(0));
  SetDataSetHidden(1, !GetCheckBoxValue(1));
    
  ChangeInfoes(0,"Day1", "(times)");
  ChangeInfoes(1,"Day2", "(times)");
  myLineChart.update()
}

function SetRetryCountGraph()
{
  RemoveAllData(myLineChart);
  AddAllLabelToChartData();

  for(var i = 0; i < jsonData[0].length; i++)
    AddData(0, jsonParsingDatas1.RetryCount[i]);

  for(var i = 0; i < jsonData[1].length; i++)
    AddData(1, jsonParsingDatas2.RetryCount[i]);

  SetDataSetHidden(0, !GetCheckBoxValue(0));
  SetDataSetHidden(1, !GetCheckBoxValue(1));
    
  ChangeInfoes(0,"Day1", "(times)");
  ChangeInfoes(1,"Day2", "(times)");
  myLineChart.update()
}

document.getElementById('QADataClear').onclick = function(){
  RemoveAllData(myLineChart);
  ChangeInfoes(0,"", "");
  ChangeInfoes(1,"", "");
};

var chartData = {
  labels: [],
  datasets: [{
    label: "PlayTime",
    lineTension: 0,
    backgroundColor: "rgba(255, 116, 115, 0.05)",
    borderColor: "rgba(255, 116, 115, 1)",
    pointRadius: 3,
    pointBackgroundColor: "rgba(255, 116, 115, 1)",
    pointBorderColor: "rgba(255, 116, 115, 1)",
    pointHoverRadius: 3,
    pointHoverBackgroundColor: "rgba(255, 116, 115, 1)",
    pointHoverBorderColor: "rgba(255, 116, 115, 1)",
    pointHitRadius: 10,
    pointBorderWidth: 2,
    data: [],
    hidden: false,
  },
  {
    label: "PlayTime",
    lineTension: 0,
    backgroundColor: "rgba(255, 201, 82, 0.05)",
    borderColor: "rgba(255, 201, 82, 1)",
    pointRadius: 3,
    pointBackgroundColor: "rgba(255, 201, 82, 1)",
    pointBorderColor: "rgba(255, 201, 82, 1)",
    pointHoverRadius: 3,
    pointHoverBackgroundColor: "rgba(255, 201, 82, 1)",
    pointHoverBorderColor: "rgba(255, 201, 82, 1)",
    pointHitRadius: 10,
    pointBorderWidth: 2,
    data: [],
    hidden: false,
  }],
}

var chartOption = {
  maintainAspectRatio: false,
  layout: {
    padding: {
      left: 10,
      right: 25,
      top: 25,
      bottom: 0
    }
  },
  scales: {
    xAxes: [{
      time: {
        unit: 'date'
      },
      gridLines: {
        display: false,
        drawBorder: false
      },
      ticks: {
        autoSkip : false,
        maxRotation : 90,
        minRotationRotation : 90,
      }
    }],
    yAxes: [{
      ticks: {
        maxTicksLimit: 10,
        padding: 10,
        // Include a dollar sign in the ticks
        callback: function(value, index, values) {
          return number_format(value);
        }
      },
      gridLines: {
        color: "rgb(234, 236, 244)",
        zeroLineColor: "rgb(234, 236, 244)",
        drawBorder: false,
        borderDash: [2],
        zeroLineBorderDash: [2]
      }
    }],
  },
  legend: {
    display: true,
    position: 'bottom'
  },
  tooltips: {
    backgroundColor: "rgb(255,255,255)",
    bodyFontColor: "#858796",
    titleMarginBottom: 10,
    titleFontColor: '#6e707e',
    titleFontSize: 14,
    borderColor: '#dddfeb',
    borderWidth: 1,
    xPadding: 15,
    yPadding: 15,
    displayColors: false,
    intersect: false,
    mode: 'index',
    caretPadding: 10,
    callbacks: {
      label: function(tooltipItem, chart) {
        var datasetLabel = chart.datasets[tooltipItem.datasetIndex].label || '';
        return datasetLabel + ': ' + number_format(tooltipItem.yLabel);
      }
    }
  }
}

// Area Chart Example
var ctx = document.getElementById("myAreaChart");
var myLineChart = new Chart(ctx, {
  type: 'line',
  data: chartData,
  options: chartOption
});


