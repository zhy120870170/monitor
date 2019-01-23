
$(function () {
    initChartWidth();
    initDatetimeRangePicker();

    // 窗口缩放后重绘图表
    $(window).on('resize', function () {
        reRenderCharts()
    })

    $("#target_info_gather").on('click', function () {
        if (this.analyzerChart && this.emotionChart) {
            reRenderCharts()
        } else {
            initCharts();
        }
    })

    // 初始化渲染日期选择控件
    function initDatetimeRangePicker() {
        var $rangeKey = $('#datetime_range_key')
        var $subInput = $('#datetime_range')
        var $dateTextContainer = $('#datetime_range_key span')

        var startDate = moment($rangeKey.data('start-date'), 'YYYY-MM-DD')
        var endDate = moment($rangeKey.data('end-date'), 'YYYY-MM-DD')

        function cb(start, end) {
            var _range
            if (end.dayOfYear() === start.dayOfYear()) {
                _range = start.format('YYYYMMDD')
            } else {
                _range = start.format('YYYYMMDD') + ' - ' + end.format('YYYYMMDD')
            }
            $dateTextContainer.html(_range)
            return $subInput.val(_range)
        }

        $rangeKey.daterangepicker({
            opens: 'right',
            startDate: startDate,
            endDate: endDate,
            minDate: moment().subtract(1, 'year'),
            maxDate: moment().add(1, 'year'),
            showDropdowns: true,
            showWeekNumbers: false,
            timePicker: false,
            autoUpdateInput: true,
            maxSpan: moment.duration(31, 'days'),
            ranges: {
                '今天': [moment(), moment()],
                '昨天': [moment().subtract('days', 1), moment().subtract('days', 1)],
                '前天': [moment().subtract('days', 2), moment().subtract('days', 2)],
                '最近7天': [moment().subtract('days', 6), moment().subtract('days')],
                '最近30天': [moment().subtract('days', 29), moment().subtract('days')]
            },
            buttonClasses: ['btn'],
            applyClass: 'green',
            cancelClass: 'default',
            format: 'YYYY/MM/DD',
            locale: {
                applyLabel: '选择',
                cancelLabel: '取消',
                fromLabel: '开始时间',
                toLabel: '结束时间',
                customRangeLabel: '自定义时间段',
                daysOfWeek: ['日', '一', '二', '三', '四', '五', '六'],
                monthNames: ['1月', '2月', '3月', '4月', '5月', '6月', '7月', '8月', '9月', '10月', '11月', '12月'],
                firstDay: 1
            }
        }, cb)

        cb(startDate, endDate)
    }

    // 初始化图标
    function initCharts() {
        initEmotionChart()

        initWordsCloudChart()
    }

    // 重绘图标
    function reRenderCharts() {
        if ($('#info_gather').is(':visible')) {
            this.analyzerChart && this.analyzerChart.resize();
            this.emotionChart && this.emotionChart.resize();
        }
    }

    // 初始化情感属性扇形图
    function initEmotionChart() {
        var legendData = ['正面', '负面', '中性'];
        var seriesData = [
            { name: '正面', value: '30'},
            { name: '负面', value: '50'},
            { name: '中性', value: '80'}
        ];
        var emotionDom = $("#chart_content_emotion")[0]
        const option = {
            title: {
                show: false
            },
            borderWidth: 2,
            tooltip: {
                trigger: 'item',
                formatter: '{a} <br/>{b} : {c} ({d}%)'
            },
            legend: {
                orient: 'horizontal',
                bottom: 20,
                icon: 'roundRect',
                x: 'center',
                textStyle: {
                    color: '#333'
                },
                data: legendData
            },
            series: [
                {
                    name: '系统分布',
                    type: 'pie',
                    radius: ['40%', '55%'],
                    center: ['50%', '50%'],
                    color: ['#0E7CE2', '#FF8352', '#E271DE', '#F8456B', '#00FFFF', '#4AEAB0'],
                    data: seriesData,
                    itemStyle: {
                        emphasis: {
                            shadowBlur: 10,
                            shadowOffsetX: 0,
                            shadowColor: 'rgba(0, 0, 0, 0.5)'
                        }
                    },
                    labelLine: {
                        normal: {
                            show: true,
                            length: 20,
                            lineStyle: {
                                width: 2
                            }
                        }
                    },
                    label: {
                        normal: {
                            formatter: '{c|{c}}\n{hr|}\n{d|{d}%}',
                            rich: {
                                b: {
                                    fontSize: 20,
                                    align: 'left',
                                    padding: 4
                                },
                                hr: {
                                    borderColor: '#12EABE',
                                    width: '100%',
                                    borderWidth: 2,
                                    height: 0
                                },
                                d: {
                                    fontSize: 20,
                                    align: 'left',
                                    padding: 4
                                },
                                c: {
                                    fontSize: 20,
                                    align: 'left',
                                    padding: 4
                                }
                            }
                        }
                    }
                }
            ]
        }
        this.emotionChart = echarts.init(emotionDom)
        this.emotionChart.setOption(option)
    }

    // 单词云
    function initWordsCloudChart() {
        var maskImage = new Image();
        var analyzerDom = $("#chart_content_analyzer")[0]

        var data = {
            value: [
                {
                    "name": "花鸟市场",
                    "value": 1446
                },
                {
                    "name": "汽车",
                    "value": 928
                },
                {
                    "name": "视频",
                    "value": 906
                },
                {
                    "name": "电视",
                    "value": 825
                },
                {
                    "name": "Lover Boy 88",
                    "value": 514
                },
                {
                    "name": "动漫",
                    "value": 486
                },
                {
                    "name": "音乐",
                    "value": 53
                },
                {
                    "name": "直播",
                    "value": 163
                },
                {
                    "name": "广播电台",
                    "value": 86
                },
                {
                    "name": "戏曲曲艺",
                    "value": 17
                },
                {
                    "name": "演出票务",
                    "value": 6
                },
                {
                    "name": "给陌生的你听",
                    "value": 1
                },
                {
                    "name": "资讯",
                    "value": 1437
                },
                {
                    "name": "商业财经",
                    "value": 422
                },
                {
                    "name": "娱乐八卦",
                    "value": 353
                },
                {
                    "name": "军事",
                    "value": 331
                },
                {
                    "name": "科技资讯",
                    "value": 313
                },
                {
                    "name": "社会时政",
                    "value": 307
                },
                {
                    "name": "时尚",
                    "value": 43
                },
                {
                    "name": "网络奇闻",
                    "value": 15
                },
                {
                    "name": "旅游出行",
                    "value": 438
                },
                {
                    "name": "景点类型",
                    "value": 957
                },
                {
                    "name": "国内游",
                    "value": 927
                },
                {
                    "name": "远途出行方式",
                    "value": 908
                },
                {
                    "name": "酒店",
                    "value": 693
                },
                {
                    "name": "关注景点",
                    "value": 611
                },
                {
                    "name": "旅游网站偏好",
                    "value": 512
                },
                {
                    "name": "出国游",
                    "value": 382
                },
                {
                    "name": "交通票务",
                    "value": 312
                },
                {
                    "name": "旅游方式",
                    "value": 187
                },
                {
                    "name": "旅游主题",
                    "value": 163
                },
                {
                    "name": "港澳台",
                    "value": 104
                },
                {
                    "name": "本地周边游",
                    "value": 3
                }
            ],
            image:"data:image/svg+xml;base64,PD94bWwgdmVyc2lvbj0iMS4wIiBzdGFuZGFsb25lPSJubyI/PjwhRE9DVFlQRSBzdmcgUFVCTElDICItLy9XM0MvL0RURCBTVkcgMS4xLy9FTiIgImh0dHA6Ly93d3cudzMub3JnL0dyYXBoaWNzL1NWRy8xLjEvRFREL3N2ZzExLmR0ZCI+PHN2ZyB0PSIxNTM5NjcxMDg4MjI5IiBjbGFzcz0iaWNvbiIgc3R5bGU9IiIgdmlld0JveD0iMCAwIDEwMjQgMTAyNCIgdmVyc2lvbj0iMS4xIiB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHAtaWQ9IjE5Njc3IiB4bWxuczp4bGluaz0iaHR0cDovL3d3dy53My5vcmcvMTk5OS94bGluayIgd2lkdGg9IjUwMCIgaGVpZ2h0PSI1MDAiPjxkZWZzPjxzdHlsZSB0eXBlPSJ0ZXh0L2NzcyI+PC9zdHlsZT48L2RlZnM+PHBhdGggZD0iTTgwNi4xMjMgMTUzLjU3OWg2NS41MzZ2NzE4LjkxMkg2ODQuMjY3VjU1Mi45Nkw1MzEuNjcgNzEyLjcyNWgtMjAuNDU5TDM1OS42NTkgNTUyLjk2djMxOS41MzFIMTcyLjI0NlYxNTMuNTc5aDY3LjU4NGwyODAuNTk3IDMxMS4zMTcgMjg1LjY5Ni0zMTEuMzE3eiIgcC1pZD0iMTk2NzgiPjwvcGF0aD48L3N2Zz4="
        }
        maskImage.src = data.image
        maskImage.onload = function() {
            this.analyzerChart = echarts.init(analyzerDom)
            this.analyzerChart.setOption({
                backgroundColor: '#fff',
                tooltip: {
                    show: false
                },
                series: [{
                    type: 'wordCloud',
                    gridSize: 1,
                    size: [6, 66],
                    tooltip: {
                        show: true
                    },
                    toolbox: {
                        feature: {
                            saveAsImage: {
                                iconStyle: {
                                    normal: {
                                        color: '#FFFFFF'
                                    }
                                }
                            }
                        }
                    },
                    rotationRange: [-90, 90],
                    // maskImage: maskImage,
                    textStyle: {
                        normal: {
                            color: function (v) {
                                let color = ['#27D38A', '#FFCA1C', '#5DD1FA', '#F88E25', '#47A0FF', '#FD6565']
                                let num = Math.floor(Math.random() * (5 + 1));
                                return color[num];
                            },
                        },
                    },
                    left: 'center',
                    top: 'center',
                    width: '80%',
                    height: '80%',
                    data: data.value
                }]
            })
        }
    }

    // 初始化图标宽度
    function initChartWidth() {
        var wWidth = (window.innerWidth - 300)/2
        $('#chart_content_emotion').css({'height': '400px', 'width': wWidth + 'px'})
        $('#chart_content_analyzer').css({'height': '400px', 'width': wWidth + 'px'})
    }

function initWordsCloudChart(word_datas) {
        var maskImage = new Image();
        var analyzerDom = $("#chart_content_analyzer")[0]
        var values = []
        for ( var i = 0; i <word_datas.length; i++){
            if(i>=100){
                break;
            }
            values.push(word_datas[i]);
        }

        var data = {
            value: values,
//            image:"static/images/test.jpg"
            image:"data:image/svg+xml;base64,PD94bWwgdmVyc2lvbj0iMS4wIiBzdGFuZGFsb25lPSJubyI/PjwhRE9DVFlQRSBzdmcgUFVCTElDICItLy9XM0MvL0RURCBTVkcgMS4xLy9FTiIgImh0dHA6Ly93d3cudzMub3JnL0dyYXBoaWNzL1NWRy8xLjEvRFREL3N2ZzExLmR0ZCI+PHN2ZyB0PSIxNTM5NjcxMDg4MjI5IiBjbGFzcz0iaWNvbiIgc3R5bGU9IiIgdmlld0JveD0iMCAwIDEwMjQgMTAyNCIgdmVyc2lvbj0iMS4xIiB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHAtaWQ9IjE5Njc3IiB4bWxuczp4bGluaz0iaHR0cDovL3d3dy53My5vcmcvMTk5OS94bGluayIgd2lkdGg9IjUwMCIgaGVpZ2h0PSI1MDAiPjxkZWZzPjxzdHlsZSB0eXBlPSJ0ZXh0L2NzcyI+PC9zdHlsZT48L2RlZnM+PHBhdGggZD0iTTgwNi4xMjMgMTUzLjU3OWg2NS41MzZ2NzE4LjkxMkg2ODQuMjY3VjU1Mi45Nkw1MzEuNjcgNzEyLjcyNWgtMjAuNDU5TDM1OS42NTkgNTUyLjk2djMxOS41MzFIMTcyLjI0NlYxNTMuNTc5aDY3LjU4NGwyODAuNTk3IDMxMS4zMTcgMjg1LjY5Ni0zMTEuMzE3eiIgcC1pZD0iMTk2NzgiPjwvcGF0aD48L3N2Zz4="
        }
        maskImage.src = data.image
        maskImage.onload = function() {
            this.analyzerChart = echarts.init(analyzerDom)
            this.analyzerChart.setOption({
                backgroundColor: '#fff',
                tooltip: {
                    show: false
                },
                series: [{
                    type: 'wordCloud',
                    gridSize: 1,
                    size: [6, 66],
                    tooltip: {
                        show: true
                    },
                    toolbox: {
                        feature: {
                            saveAsImage: {
                                iconStyle: {
                                    normal: {
                                        color: '#FFFFFF'
                                    }
                                }
                            }
                        }
                    },
                    rotationRange: [-90, 90],
//                    maskImage: maskImage,
                    textStyle: {
                        normal: {
                            color: function (v) {
                                let color = ['#27D38A', '#FFCA1C', '#5DD1FA', '#F88E25', '#47A0FF', '#FD6565']
                                let num = Math.floor(Math.random() * (5 + 1));
                                return color[num];
                            },
                        },
                    },
                    left: 'center',
                    top: 'center',
                    width: '80%',
                    height: '80%',
                    data: data.value
                }]
            })
        }
    }
})
