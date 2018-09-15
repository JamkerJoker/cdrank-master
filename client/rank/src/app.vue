<template>
    <div id='main' class='main'>
        <Alert type="success" show-icon closable>
            版本更新提示 2018-9-13
            <span slot="desc">新增东北地区航班预警，可查询东北地区航班机场离港率以及最新排名 </span>
        </Alert>

        <Row>
            <i-col span="8">
                <img width="210px" height="70px"  align="left" src="./images/logo1.jpg">
            </i-col>
            <i-col span="8">
                <h1 style="line-height:70px;text-align: center">
                    成都航空运行控制中心航班预警排名系统
                </h1>
                <marquee>
                    WELCOME TO USE  CHENGDU AIRLINES RANK WARNING SYSTEM.<br>
                </marquee>
            </i-col>
            <i-col span="8">
                <img width="210px" height="70px" align="right" src="./images/logo2.jpg">
            </i-col>
        </Row>
        <Row>
            <i-col span="7">
                <div class='list'>
                    <Row>
                        <i-col span='3'>
                            <Select
                                    v-model='org'
                                    placeholder='机构'
                                    filterable>
                                <Option v-for='(item, index) in orgs' :value='item' :key='index'>{{ item }}</Option>
                            </Select>
                        </i-col>
                        <i-col span='1'>
                            &nbsp;
                        </i-col>
                        <i-col span='4'>
                            <Select
                                    v-model='flight'
                                    clearable
                                    placeholder='航班号'
                                    filterable>
                                <Option v-for='(item, index) in flights' :value='item' :key='index'>{{ item }}</Option>
                            </Select>
                        </i-col>
                        <i-col span='1'>
                            &nbsp;
                        </i-col>
                        <i-col span='4'>
                            <Select
                                    v-model='orgAirport'
                                    clearable
                                    placeholder='起飞机场'
                                    filterable>
                                <Option v-for='(item, index) in orgAirports' :value='item' :key='index'>{{ item }}</Option>
                            </Select>
                        </i-col>
                        <i-col span='1'>
                            &nbsp;
                        </i-col>
                        <i-col span='4'>
                            <Poptip trigger="hover" word-wrap width="200" content="输入目的地机场相关信息，点击右侧查询按钮即可查询您所需目的地机场的所有相关信息">
                            <Select
                                    v-model='dstAirport'
                                    clearable
                                    placeholder='降落机场'
                                    filterable>
                                <Option v-for='(item, index) in dstAirports' :value='item' :key='index'>{{ item }}</Option>
                            </Select>
                            </Poptip>
                        </i-col>
                        <i-col span='1'>
                            &nbsp;
                        </i-col>
                        <i-col span='4'>
                            <Poptip trigger="hover" word-wrap width="200" content="单点查询按钮即可查询最新航班信息">

                            <Button
                                    type='primary'
                                    long
                                    @click='handleSearch'>
                                查询
                            </Button>
                            </Poptip>
                        </i-col>
                    </Row>
                    <br>

                    <Table
                            :columns='rankColumns'
                            :data='rankRows'
                            size='small'
                            height="750"
                            :loading="loading"
                            @on-row-click="handleClick"
                            highlight-row
                            ref='table'>
                    </Table>
                </div>
            </i-col>
            <i-col span="17">
                <div v-if="org === '总局'" id='chartAviation' class='chart' key="div1">
                    <Card style="height: 400px" :padding="0">
                        <div style="width:calc(100%);height: 400px">
                            <scatter :scatterData="scatterData" key="1">
                            </scatter>
                        </div>
                    </Card>
                    <br>
                    <Card style="height: 400px" :padding="0">
                        <div style="width:calc(100%);height: 400px">
                            <pie :pieData="pieData">
                            </pie>
                        </div>
                    </Card>
                    <br>
                    <Card style="height: 600px" :padding="0">
                        <Row>
                            <i-col span="16">
                                <spread :spreadData="spreadData">
                                </spread>
                            </i-col>
                            <i-col span="8">
                                <div style="width:calc(100%);height: 400px">
                                    <radar :radarData="radarData">
                                    </radar>
                                </div>
                            </i-col>
                        </Row>
                        <Row>
                            <br>
                            <br>
                            <Method>
                                </Method>
                        </Row>
                    </Card>

                </div>
                <div v-if="org === '华东'" id='chartEast' class='chart' key="div2">
                <Card style="height: 800px" :padding="0">
                    <div style="width: calc(100%);height: 800px">
                        <scatter :scatterData="scatterData" key="2">
                        </scatter>
                    </div>
                </Card>
            </div>

                <div v-if="org === '东北'" id='chartNorthEast' class='chart' key="div3">
                    <Card style="height: 800px" :padding="0">
                        <div style="width: calc(100%);height: 800px">
                            <scatter :scatterData="scatterData" key="3">
                            </scatter>
                        </div>
                    </Card>
                </div>
            </i-col>

        </Row>
    </div>
</template>

<script>
    import {fetchEast, fetchLastEast, fetchAviation, fetchReason,fetchNorthEast,fetchLastNorthEast} from './api/rank';
    import scatter from './components/scatter';
    import pie from './components/pie';
    import spread from './components/spread';
    import radar from './components/radar';
    import util from './libs/util';
    import Method from "./components/Method";

    export default {
        components: {
            Method,
            scatter,
            pie,
            spread,
            radar
        },
        data () {
            return {
                hSplit: 0.3,
                eastData: [],
                eastLastData: [],
                aviationData: [],
                reasonData: [],
                NorthEastData:[],
                NorthEastLastData:[],
                orgs: ['华东', '总局','东北'],
                org: '总局',
                flights: [],
                flight: '',
                orgAirports: [],
                orgAirport: '',
                dstAirports: [],
                dstAirport: '',
                loading: false,
                rankColumns: [],
                rankRows: [],
                rankData: [],
                currentb: 0,
                currenty: 0,
                currento: 0,
                currentr: 0,


                eastRankColumns: [
                    {
                        type: 'index',
                        width: 50,
                        align: 'center'
                    },
                    {
                        'title': '航班号',
                        'key': 'flight',
                        'width': 110,
                        'sortable': true

                    },
                    {
                        'title': '起飞机场',
                        'key': 'orgAirport',
                        'width': 110,
                        'sortable': true
                    },
                    {
                        'title': '降落机场',
                        'key': 'dstAirport',
                        'width': 110,
                        'sortable': true
                    },
                    {
                        'title': '离港率',
                        'key': 'rate',
                        'width': 110,
                        'sortable': true
                    },
                    {
                        'title': '最新排名',
                        'key': 'rank',
                        'width': 110,
                        'sortable': true
                    },
                    {
                        'title': '上个月排名',
                        'key': 'lastRank',
                        'width': 150,
                        'sortable': true
                    },
                    {
                        'title': '上上个月排名',
                        'key': 'lastLastRank',
                        'width': 150,
                        'sortable': true
                    }
                ],

                EastNorthRankColumns: [
                    {
                        type: 'index',
                        width: 50,
                        align: 'center'
                    },
                    {
                        'title': '航班号',
                        'key': 'flight',
                        'width': 110,
                        'sortable': true

                    },
                    {
                        'title': '起飞机场',
                        'key': 'orgAirport',
                        'width': 110,
                        'sortable': true
                    },
                    {
                        'title': '降落机场',
                        'key': 'dstAirport',
                        'width': 110,
                        'sortable': true
                    },
                    {
                        'title': '离港率',
                        'key': 'rate',
                        'width': 110,
                        'sortable': true
                    },
                    {
                        'title': '最新排名',
                        'key': 'rank',
                        'width': 110,
                        'sortable': true
                    },
                    {
                        'title': '上个月排名',
                        'key': 'lastRank',
                        'width': 150,
                        'sortable': true
                    },
                    {
                        'title': '上上个月排名',
                        'key': 'lastLastRank',
                        'width': 150,
                        'sortable': true
                    }

                ],

                aviationRankColumns: [
                    {
                        type: 'index',
                        width: 50,
                        align: 'center'
                    },
                    {
                        'title': '航班号',
                        'key': 'flight',
                        'width': 110,
                        'sortable': true
                    },
                    {
                        'title': '起飞机场',
                        'key': 'orgAirport',
                        'width': 110,
                        'sortable': true
                    },
                    {
                        'title': '降落机场',
                        'key': 'dstAirport',
                        'width': 110,
                        'sortable': true
                    },
                    {
                        'title': '最新排名',
                        'key': 'rank',
                        'width': 110,
                        'sortable': true
                    },
                    {
                        'title': '正常率',
                        'key': 'rate',
                        'width': 110,
                        'sortable': true
                    },


                ],


                items: [],
                scatterData: [],
                pieData: [],
                spreadData: [],
                radarData: []
            };
        },
        mounted () {
            fetchAviation().then(response => {
                this.aviationData = response.data;
                this.resetInputFields();
                this.handleSearch();
            });
            fetchReason().then(response => {
                this.reasonData = response.data;
            });
            fetchLastEast().then(response => {
                this.eastLastData = response.data;
            });
            fetchNorthEast().then(response => {
                this.NorthEastData= response.data;

            });
            fetchLastNorthEast().then(response => {
                this.NorthEastLastData= response.data;

            });

        },
        beforeDestroy () {
        },
        watch: {
            'org': function (data) {
                if (data === '总局') {
                    fetchAviation().then(response => {
                        this.aviationData = response.data;
                        this.resetInputFields();
                    });
                }
                if (data === '华东')
                {
                    fetchEast().then(response => {
                        this.eastData = response.data;
                        this.resetInputFields();
                    });
                }
                if (data === '东北')
                {
                    fetchNorthEast.then(response => {
                        this.NorthEastData = response.data;
                        this.resetInputFields();
                    });
                }
            }
        },
        methods: {
            Blue () {
                if (this.currentb == 3) {
                    this.currentb = 0;
                } else {
                    this.currentb += 1;
                }
            },
            Yellow () {
                if (this.currenty == 5) {
                    this.currenty = 0;
                } else {
                    this.currenty += 1;
                }
            },
            Orange () {
                if (this.currento == 6) {
                    this.currento = 0;
                } else {
                    this.currento += 1;
                }
            },
            Red () {
                if (this.currentr == 7) {
                    this.currentr = 0;
                } else {
                    this.currentr += 1;
                }
            },
            resetInputFields () {
                let jsonData = null;
                let tmpFlights = [];
                let tmpOrgAirports = [];
                let tmpDstAirports = [];

                if (this.org === '华东') {
                    jsonData = this.eastData;
                }
                if (this.org === '总局')
                {
                    jsonData = this.aviationData;
                }
                if (this.org === '东北')
                {
                    jsonData = this.NorthEastData;
                }
                for (let dateKey in jsonData) {
                    let dateValue = jsonData[dateKey];
                    dateValue.map(ranks => {
                        ranks.map(rank => {
                            // 航班号
                            let flight = rank.fnum;
                            if (!util.oneOf(flight, tmpFlights)) {
                                tmpFlights.push(flight);
                            }

                            // 起飞机场
                            let orgAirport = rank.forg;
                            if (!util.oneOf(orgAirport, tmpOrgAirports)) {
                                tmpOrgAirports.push(orgAirport);
                            }

                            // 降落机场
                            let dstAirport = rank.fdst;
                            if (!util.oneOf(dstAirport, tmpDstAirports)) {
                                tmpDstAirports.push(dstAirport);
                            }
                        });
                    });
                }
                this.flights = tmpFlights;
                this.orgAirports = tmpOrgAirports;
                this.dstAirports = tmpDstAirports;

                this.flight = '';
                this.orgAirport = '';
                this.dstAirport = '';
            },
            handleSearch () {
                this.loading = true;
                if (this.org === '华东') {
                    setTimeout(() => {
                        this.setEastRankData(this.eastData);
                    }, 250);
                }
                if (this.org === '总局')
                {
                    setTimeout(() => {
                        this.setAviationRankData(this.aviationData);
                    }, 250);
                }
                if (this.org === '东北')
                {
                    setTimeout(() => {
                        this.setEastNorthRankData(this.NorthEastData);
                    }, 250);
                }
            },
            getReason (rank) {
                let fnum = rank.flight;
                let forg = rank.orgAirport;
                let fdst = rank.dstAirport;
                let date = rank.date;
                let rs = '';
                for (let reason of this.reasonData) {
                    if (reason.fnum === fnum &&
                        reason.forg === forg &&
                        reason.fdst === fdst &&
                        reason.ScheduledDate === date) {
                        let reasonCode = reason.UnnormalReason.substr(0, 2);
                        switch (reasonCode) {
                            case '01':
                                rs = '天气';
                                break;
                            case '02':
                                rs = '公司';
                                break;
                            case '03':
                                rs = '空管';
                                break;
                            case '04':
                                rs = '军事';
                                break;
                            default:
                                rs = '其他';
                                break;
                        }
                        break;
                    }
                }
                return rs;
            },

            getEastNorthLastRank (flightArg, orgAirportArg, dstAirportArg) {
                let tmpRankData = [];
                for (let dateKey in this.NorthEastLastData) {
                    let dateValue = this.NorthEastLastData[dateKey];
                    dateValue.map(ranks => {
                        ranks.map(rank => {
                            // 航班号
                            let flight = rank.fnum;
                            // 起飞机场
                            let orgAirport = rank.forg;
                            // 降落机场
                            let dstAirport = rank.fdst;

                            // 排名列表
                            let canPush = false;
                            if (flightArg === flight) {
                                if (orgAirportArg === orgAirport) {
                                    if (dstAirportArg === dstAirport) {
                                        canPush = true;
                                    }
                                }
                            }
                            if (canPush) {
                                tmpRankData.push({
                                    date: dateKey,
                                    flight: flight,
                                    orgAirport: orgAirport,
                                    dstAirport: dstAirport,
                                    rank: ('00000' + rank.ranking).slice(-3)
                                });
                            }
                        });
                    });
                }
                return tmpRankData;
            },
            setEastNorthRankData (jsonData) {
                this.rankColumns = this.EastNorthRankColumns;
                let tmpRankRows = [];
                let tmpRankData = [];

                for (let dateKey in jsonData) {
                    let dateValue = jsonData[dateKey];
                    dateValue.map(ranks => {
                        ranks.map(rank => {
                            // 航班号
                            let flight = rank.fnum;
                            // 起飞机场
                            let orgAirport = rank.forg;
                            // 降落机场
                            let dstAirport = rank.fdst;
                            // 上个月排名以及上上个月排名
                            let lastRank = this.getEastNorthLastRank(flight, orgAirport, dstAirport);
                            // 排名列表
                            let canPush = false;
                            if (util.isNull(this.flight) ||
                                this.flight === '' ||
                                this.flight === flight) {
                                if (util.isNull(this.orgAirport) ||
                                    this.orgAirport === '' ||
                                    this.orgAirport === orgAirport) {
                                    if (util.isNull(this.dstAirport) ||
                                        this.dstAirport === '' ||
                                        this.dstAirport === dstAirport) {
                                        canPush = true;
                                    }
                                }
                            }
                            if (canPush) {
                                tmpRankData.push({
                                    date: dateKey,
                                    flight: flight,
                                    orgAirport: orgAirport,
                                    dstAirport: dstAirport,
                                    rank: rank.ranking
                                });
                                canPush = true;
                                for (let rankRow of tmpRankRows) {
                                    if (rankRow.flight === flight &&
                                        rankRow.orgAirport === orgAirport &&
                                        rankRow.dstAirport === dstAirport) {
                                        if (dateKey > rankRow.date) {
                                            rankRow.rank = ('00000' + rank.ranking).slice(-3);
                                            rankRow.rate = (rank.normalRate * 100).toFixed(1)+'%';
                                        }
                                        canPush = false;
                                    }
                                }
                                if (canPush) {
                                    tmpRankRows.push({
                                        date: dateKey,
                                        flight: flight,
                                        orgAirport: orgAirport,
                                        dstAirport: dstAirport,
                                        rank: ('00000' + rank.ranking).slice(-3),
                                        rate: (rank.normalRate * 100).toFixed(1)+'%',
                                        lastRank: lastRank.length === 3 ? lastRank[1].rank : 0,
                                        lastLastRank: lastRank.length === 3 ? lastRank[0].rank : 0
                                    });
                                }
                            }
                        });
                    });
                }
                this.rankRows = tmpRankRows;
                this.rankData = tmpRankData;
                this.loading = false;
                this.scatterData = [];
            },
            getEastLastRank (flightArg, orgAirportArg, dstAirportArg) {
                let tmpRankData = [];
                for (let dateKey in this.eastLastData) {
                    let dateValue = this.eastLastData[dateKey];
                    dateValue.map(ranks => {
                        ranks.map(rank => {
                            // 航班号
                            let flight = rank.fnum;
                            // 起飞机场
                            let orgAirport = rank.forg;
                            // 降落机场
                            let dstAirport = rank.fdst;

                            // 排名列表
                            let canPush = false;
                            if (flightArg === flight) {
                                if (orgAirportArg === orgAirport) {
                                    if (dstAirportArg === dstAirport) {
                                        canPush = true;
                                    }
                                }
                            }
                            if (canPush) {
                                tmpRankData.push({
                                    date: dateKey,
                                    flight: flight,
                                    orgAirport: orgAirport,
                                    dstAirport: dstAirport,
                                    rank: ('00000' + rank.ranking).slice(-3)
                                });
                            }
                        });
                    });
                }
                return tmpRankData;
            },
            setEastRankData (jsonData) {
                this.rankColumns = this.eastRankColumns;
                let tmpRankRows = [];
                let tmpRankData = [];

                for (let dateKey in jsonData) {
                    let dateValue = jsonData[dateKey];
                    dateValue.map(ranks => {
                        ranks.map(rank => {
                            // 航班号
                            let flight = rank.fnum;
                            // 起飞机场
                            let orgAirport = rank.forg;
                            // 降落机场
                            let dstAirport = rank.fdst;
                            // 上个月排名以及上上个月排名
                            let lastRank = this.getEastLastRank(flight, orgAirport, dstAirport);
                            // 排名列表
                            let canPush = false;
                            if (util.isNull(this.flight) ||
                                this.flight === '' ||
                                this.flight === flight) {
                                if (util.isNull(this.orgAirport) ||
                                    this.orgAirport === '' ||
                                    this.orgAirport === orgAirport) {
                                    if (util.isNull(this.dstAirport) ||
                                        this.dstAirport === '' ||
                                        this.dstAirport === dstAirport) {
                                        canPush = true;
                                    }
                                }
                            }
                            if (canPush) {
                                tmpRankData.push({
                                    date: dateKey,
                                    flight: flight,
                                    orgAirport: orgAirport,
                                    dstAirport: dstAirport,
                                    rank: rank.ranking
                                });
                                canPush = true;
                                for (let rankRow of tmpRankRows) {
                                    if (rankRow.flight === flight &&
                                        rankRow.orgAirport === orgAirport &&
                                        rankRow.dstAirport === dstAirport) {
                                        if (dateKey > rankRow.date) {
                                            rankRow.rank = ('00000' + rank.ranking).slice(-3);

                                        }
                                        canPush = false;
                                    }
                                }
                                if (canPush) {
                                    tmpRankRows.push({
                                        date: dateKey,
                                        flight: flight,
                                        orgAirport: orgAirport,
                                        dstAirport: dstAirport,
                                        rank: ('00000' + rank.ranking).slice(-3),
                                        rate: (rank.normalRate * 100).toFixed(1)+'%',
                                        lastRank: lastRank.length === 3 ? lastRank[1].rank : 0,
                                        lastLastRank: lastRank.length === 3 ? lastRank[0].rank : 0
                                    });
                                }
                            }
                        });
                    });
                }
                this.rankRows = tmpRankRows;
                this.rankData = tmpRankData;
                this.loading = false;
                this.scatterData = [];
            },
            setAviationRankData (jsonData) {
                this.rankColumns = this.aviationRankColumns;
                let tmpRankRows = [];
                let tmpRankData = [];

                for (let dateKey in jsonData) {
                    let dateValue = jsonData[dateKey];
                    dateValue.map(ranks => {
                        ranks.map(rank => {
                            // 航班号
                            let flight = rank.fnum;
                            // 起飞机场
                            let orgAirport = rank.forg;
                            // 降落机场
                            let dstAirport = rank.fdst;

                            // 排名列表

                            let canPush = false;
                            if (util.isNull(this.flight) ||
                                this.flight === '' ||
                                this.flight === flight) {
                                if (util.isNull(this.orgAirport) ||
                                    this.orgAirport === '' ||
                                    this.orgAirport === orgAirport) {
                                    if (util.isNull(this.dstAirport) ||
                                        this.dstAirport === '' ||
                                        this.dstAirport === dstAirport) {

                                        canPush = true;
                                    }
                                }
                            }
                            if (canPush) {
                                tmpRankData.push({
                                    date: dateKey,
                                    flight: flight,
                                    orgAirport: orgAirport,
                                    dstAirport: dstAirport,
                                    rank: rank.ranking,
                                    weather: rank['天气'],
                                    company: rank['公司'],
                                    flow: rank['流量'],
                                    military: rank['军事活动'],
                                    airControl: rank['空管'],
                                    airport: rank['机场'],
                                    unionCheck: rank['联检'],
                                    oil: rank['油料'],
                                    departSystem: rank['离港系统'],
                                    passenger: rank['旅客'],
                                    security: rank['公共安全'],
                                    delayTime: rank.delayTime,

                                });
                                canPush = true;
                                for (let rankRow of tmpRankRows) {
                                    if (rankRow.flight === flight &&
                                        rankRow.orgAirport === orgAirport &&
                                        rankRow.dstAirport === dstAirport) {
                                        if (dateKey > rankRow.date) {
                                            rankRow.rank = ('00000' + rank.ranking).slice(-3);
                                            rankRow.rate = (rank.normalRate * 100).toFixed(1)+'%';
                                        }
                                        canPush = false;
                                    }
                                }
                                if (canPush) {
                                    tmpRankRows.push({
                                        date: dateKey,
                                        flight: flight,
                                        orgAirport: orgAirport,
                                        dstAirport: dstAirport,
                                        rank: ('00000' + rank.ranking).slice(-3),
                                        rate:(rank.normalRate * 100).toFixed(1)+'%',
                                    });
                                }
                            }
                        });
                    });
                }
                this.rankRows = tmpRankRows;
                this.rankData = tmpRankData;
                this.loading = false;
                this.scatterData = [];
            },
            handleClick (data, index) {
                 //this.title = data.flight + '[' + data.orgAirport + ' - ' + data.dstAirport + ']';
                this.setScatterData(data);
                this.setPieData(data);
                this.setSpreadData(data);
                this.setRadarData(data);
            },
            setScatterData (data) {
                let tmp = [];
                this.rankData.map(rank => {
                    if (rank.flight === data.flight &&
                    rank.orgAirport === data.orgAirport &&
                    rank.dstAirport === data.dstAirport) {
                        let ranking = rank.rank;
                        let day = parseInt(rank.date.substr(8), 10);
                        tmp.push([day, ranking]);
                    }
                });
                this.scatterData = tmp;
            },
            setPieData (data) {
                let tmp = [];
                let tmpDay = ['day'];
                let tmpWeather = ['天气'];
                let tmpCompany = ['公司'];
                let tmpMilitary = ['军事活动'];
                let tmpAirControl = ['空管'];
                let tmpOther = ['其他'];
                this.rankData.map(rank => {
                    if (rank.flight === data.flight &&
                        rank.orgAirport === data.orgAirport &&
                        rank.dstAirport === data.dstAirport) {
                        let day = rank.date.substr(8);
                        tmpDay.push(day);
                        tmpWeather.push(rank.weather);
                        tmpCompany.push(rank.company);
                        tmpMilitary.push(rank.military);
                        tmpAirControl.push(rank.airControl);
                        tmpOther.push(rank.flow + rank.airport + rank.unionCheck + rank.oil + rank.departSystem + rank.passenger + rank.security);
                    }
                });
                tmp.push(tmpDay);
                tmp.push(tmpWeather);
                tmp.push(tmpCompany);
                tmp.push(tmpMilitary);
                tmp.push(tmpAirControl);
                tmp.push(tmpOther);

                this.pieData = tmp;
            },
            setSpreadData (data) {
                let tmp = [];
                this.rankData.map(rank => {
                    if (rank.flight === data.flight &&
                        rank.orgAirport === data.orgAirport &&
                        rank.dstAirport === data.dstAirport) {
                        let reason = this.getReason(rank);
                        rank.reason = reason;
                        tmp.push(rank);
                    }
                });
                this.spreadData = tmp;
            },
            setRadarData (data) {
                let tmpData = [];
                this.rankData.map(rank => {
                    if (rank.flight === data.flight &&
                        rank.orgAirport === data.orgAirport &&
                        rank.dstAirport === data.dstAirport) {
                        tmpData.push(rank);
                    }
                });

                let tmp = [];
                let tmpValue = [];
                let tmpName = '';

                if (tmpData.length > 0) {
                    let rank = tmpData[tmpData.length - 1];
                    tmpName = rank.date;
                    tmpValue.push(rank.weather);
                    tmpValue.push(rank.company);
                    tmpValue.push(rank.airControl);
                    tmpValue.push(rank.military);
                    tmpValue.push(rank.flow + rank.airport + rank.unionCheck + rank.oil + rank.departSystem + rank.passenger + rank.security);
                }
                tmp.push({
                    value: tmpValue,
                    name: tmpName
                });

                this.radarData = tmp;
                console.log(this.radarData);
            }
        }
    };
</script>

<style scoped>
    .main {
        /*border: 1px solid #dcdee2;*/
        /*width: 800px;*/
        height: 100%;
        font-size: small;
    }

    .list {
        padding: 10px;
        height: 850px;
        font-size: x-large;
    }

    .chart {
        height: 850px;
        padding: 10px;
        overflow-y: auto;
        font-size: medium;
    }
</style>
