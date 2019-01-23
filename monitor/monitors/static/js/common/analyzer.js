
$(function () {
    initDatetimeRangePicker();
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
})
