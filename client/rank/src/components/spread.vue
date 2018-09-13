<template>
    <div id='spread' class='spread'>
        <Table
                highlight-row
                :columns="spreadColumns"
                height="550"
                size='large'
                :row-class-name="rowClassName"
                :data="spreadRows">
        </Table>


    </div>
</template>

<script>
    export default {
        name: 'spread',
        props: {
            spreadData: {
                type: Array,
                default: []
            }
        },
        data () {
            return {
                spreadColumns: [
                    {
                        type: 'index',
                        width: 60,
                        align: 'center'
                    },
                    {
                        title: '日期',
                        key: 'date',
                        'sortable': true,

                    },
                    {
                        title: '延误原因',
                        key: 'reason'
                    },
                    {
                        title: '总延误时间',
                        key: 'delay'
                    },
                    {
                        title: '预警指数',
                        key: 'score'
                    }
                ],
                spreadRows: [],
                current:0
            };
        },
        watch: {
            'spreadData': function (data) {
                let tmp = [];
                data.map(d => {
                    let date = d.date;
                    let sumReason = d.weather + d.company + d.flow +
                        d.military + d.airControl + d.airport +
                        d.unionCheck + d.oil + d.departSystem +
                        d.passenger + d.security;
                    let reasonRate = 0.0;
                    if (sumReason > 0) {
                        reasonRate = d.company / sumReason * 100;
                    }
                    let rank = d.rank;
                    let score = this.getScore(date, reasonRate, rank);
                    let delay = d.delayTime/60+"分钟";
                    let cellClassName = {
                        score: 'scoreBlack'
                    };
                    if (score >= 90) {
                        cellClassName = {
                            score: 'scoreRed'
                        };
                        this.renderFuncRed ()
                    } else if (score >= 85 && score <= 89) {
                        cellClassName = {
                            score: 'scoreOrange'
                        };
                        this.renderFunOrange ()
                    } else if (score >= 80 && score <= 84   ) {
                        cellClassName = {
                            score: 'scoreYellow'
                        };
                        this.renderFuncYellow ()

                    } else if (score >= 70 && score <= 79) {
                        cellClassName = {
                            score: 'scoreBlue'
                        };

                    }
                    tmp.push({
                        date: date,
                        reason: d.reason,
                        delay: delay,
                        score: score,
                        cellClassName: cellClassName
                    });
                });
                this.spreadRows = this.sort(tmp);
            }
        },
        mounted () {
        },
        methods: {
            getDay(num, str) {
                let today = new Date();
                let nowTime = today.getTime();
                let ms = 24*3600*1000*num;
                today.setTime(parseInt(nowTime + ms));
                let oYear = today.getFullYear();
                let oMoth = (today.getMonth() + 1).toString();
                if (oMoth.length <= 1)
                {
                    oMoth = '0' + oMoth;
                }
                let oDay = today.getDate().toString();
                if (oDay.length <= 1)
                {
                    oDay = '0' + oDay;
                }
                return oYear + str + oMoth + str + oDay;
            },
            renderFuncYellow () {
                this.$Notice.warning({
                    title: '航班预警等级通知',
                    desc: '该航班处于黄色预警状态，请注意',
                    duration: 5

                });
            },
            renderFunOrange () {
                this.$Notice.warning({
                    title: '航班预警等级通知',
                    desc: '该航班处于橙色预警状态，请注意',
                    duration: 8

                });
            },
            renderFuncRed () {
                this.$Notice.warning({
                    title: '航班预警等级通知',
                    desc: '该航班处于红色预警状态，请注意',
                    duration: 10
                });
            },

            rowClassName (row, index) {
                if (index === 0) {
                    return 'demo-table-info-row';
                }

            },
            sort (data) {
                for (let i = 0; i < data.length; i++) {
                    for (let j = 0; j < data.length - i - 1; j++) {
                        let cur = data[j];
                        let nxt = data[j + 1];
                        if (cur.date < nxt.date) {
                            data[j] = nxt;
                            data[j + 1] = cur;
                        }
                    }
                }
                return data;
            },
            getScore (date, reasonRate, rank) {
                let day = parseInt(date.substr(8), 10);
                let score1 = 0;
                if (day === 1) {
                    score1 = 0;
                } else if (day === 2) {
                    score1 = 4;
                } else if (day === 3) {
                    score1 = 8;
                } else if (day === 4) {
                    score1 = 12;
                } else if (day === 5) {
                    score1 = 16;
                } else if (day === 6) {
                    score1 = 20;
                } else if (day === 7) {
                    score1 = 22;
                } else if (day === 8) {
                    score1 = 24;
                } else if (day === 9) {
                    score1 = 26;
                } else if (day === 10) {
                    score1 = 28;
                } else if (day === 11) {
                    score1 = 30;
                } else if (day === 12) {
                    score1 = 31;
                } else if (day === 13) {
                    score1 = 32;
                } else if (day === 14) {
                    score1 = 33;
                } else if (day === 15) {
                    score1 = 34;
                } else if (day === 16) {
                    score1 = 35;
                } else if (day === 17) {
                    score1 = 36;
                } else if (day === 18) {
                    score1 = 37;
                } else if (day === 19) {
                    score1 = 38;
                } else if (day === 20) {
                    score1 = 39;
                } else {
                    score1 = 40;
                }

                let score2 = 0;
                if (reasonRate < 20) {
                    score2 = 0;
                } else if (reasonRate >= 20 && reasonRate <= 30) {
                    score2 = 5;
                } else if (reasonRate >= 31 && reasonRate <= 35) {
                    score2 = 8;
                } else if (reasonRate >= 36 && reasonRate <= 40) {
                    score2 = 13;
                } else if (reasonRate >= 41 && reasonRate <= 45) {
                    score2 = 15;
                } else if (reasonRate >= 46 && reasonRate <= 50) {
                    score2 = 16;
                } else if (reasonRate >= 51 && reasonRate <= 60) {
                    score2 = 17;
                } else if (reasonRate >= 61 && reasonRate <= 70) {
                    score2 = 18;
                } else if (reasonRate >= 71 && reasonRate <= 80) {
                    score2 = 19;
                } else {
                    score2 = 20;
                }

                let score3 = 0;
                if (rank >= 1 && rank <= 5) {
                    score3 = 40;
                } else if (rank >= 6 && rank <= 10) {
                    score3 = 38;
                } else if (rank >= 11 && rank <= 15) {
                    score3 = 35;
                } else if (rank >= 16 && rank <= 18) {
                    score3 = 32;
                } else if (rank >= 19 && rank <= 22) {
                    score3 = 28;
                } else if (rank >= 23 && rank <= 25) {
                    score3 = 25;
                } else if (rank >= 26 && rank <= 30) {
                    score3 = 20;
                } else if (rank >= 30 && rank <= 40) {
                    score3 = 10;
                } else {
                    score3 = 0;
                }

                return score1 + score2 + score3;
            }

        }
    };
</script>

<style>
    .spread {
        height: 100%;
        width: calc(100% - 50px);
        padding-left: 50px;
        padding-top: 20px;
        transition: all 0.5s linear;
    }
    .ivu-table .scoreBlack {
        color: black;
        font-weight: bold;
    }
    .ivu-table .scoreRed {
        color: red;
        font-weight: bold;
    }
    .ivu-table .scoreOrange {
        color: orange;
        font-weight: bold;
    }
    .ivu-table .scoreYellow {
        color: yellow;
        font-weight: bold;
    }
    .ivu-table .scoreBlue {
        color: deepskyblue;
        font-weight: bold;
    }
    .ivu-table .demo-table-info-row td {
        background-color: #2db7f5;
        color: #fff;
    }

</style>
