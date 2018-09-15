<template>
    <i-col span="24">
        <h2 style="line-height:70px;text-align: center">
            蓝色预警响应措施
        </h2>
        <Steps :current="currentb">
            <Step title="措施1" icon="ios-plane" content="对预警航班进行全面分析，主要包括航班结构、航班时刻、流量限制情况、天气情况等影响航班正常运行的因素。"></Step>
            <Step title="措施2" icon="ios-paper-plane" content="根据分析情况，准确判断航班正常率发展趋势，如有正常率或机场排名有下降趋势应通过公司生产例会、航前讲解等方式向各保障部门以及各保障部门所联系外委单位要求该航班需要重点关注，同时区域经理在每日航班保障过程中严格保障各环节保障航班正常，避免出现更高级别的预警。"></Step>
            <Step title="措施3" icon="md-person-add" content="航班保障次日在民航局网站对统计有异议的航班进行申诉处理。 "></Step>
            <Step title="完成" icon="md-checkmark" status="finish" ></Step>
        </Steps>
        <br>
        <br>
        <Button type="primary" @click="Blue">措施检查</Button>

        <h2 style="line-height:70px;text-align: center">
            黄色预警响应措施
        </h2>
        <Steps :current="currenty" >
            <Step title="措施1" icon="ios-plane" content="对预警航班进行全面分析，主要包括航班结构、航班时刻、流量限制情况、天气情况等影响航班正常运行的因素。并指派专人（部门级别干部一人、区域经理一人）对该航班重点关注、分析，并给提高航班正常率的可行性方案，形成书面报告。 "></Step>
            <Step title="措施2" icon="ios-paper-plane" content="通过生产例会、签派提示、航前讲解等渠道向各保障部门以及各部门所联系外委单位要求该航班需重点保障。 "></Step>
            <Step title="措施3" icon="md-person-add" content="由部门牵头与该航班所涉及管制部门、机场保障部门进行协调。 "></Step>
            <Step title="措施4" icon="ios-hammer" content="区域经理在值班期间对备份运力的使用优先考虑黄色预警航班。 "></Step>
            <Step title="措施5" icon="md-trending-up content="在航班保障的次日在民航局网站对统计有异议的航班进行申诉处理。  "></Step>
            <Step title="完成" icon="md-checkmark" status="finish" ></Step>
        </Steps>
        <br>
        <br>
        <Button type="primary" @click="Yellow">措施检查</Button>
        <h2 style="line-height:70px;text-align: center">
            橙色预警响应措施
        </h2>
        <Steps :current="currento">
            <Step title="措施1" icon="ios-plane" content="对预警航班进行全面分析，主要包括航班结构、航班时刻、流量限制情况、天气情况等影响航班正常运行的因素。并指派专人（部门级别干部一人、区域经理一人）对该航班重点关注、分析，并给提高航班正常率的可行性方案，形成书面报告。 "></Step>
            <Step title="措施2" icon="ios-paper-plane" content="由部门牵头部门领导带队赴涉及该航班的相关管制单位、机场保障部门进行沟通协调。派出外站协调员赴当地管制单位进行协调工作。 "></Step>
            <Step title="措施3" icon="md-person-add" content="组织各生产保障部门召开运行协调会，根据航班分析报告结合各对部门保障要求形成预警航班保障方案。该保障方案需形成公司级文件下发至各部门以及各部门所联系的外委单位。 "></Step>
            <Step title="措施4" icon="ios-hammer" content="区域经理对每日公司航班结构进行分析，查找是否有换机通道，尽量避免飞机晚到导致预警航班顺延。 "></Step>
            <Step title="措施5" icon="md-trending-up" content="区域经理在值班过程中对预警航班以及涉及前序航班运行情况向运行总监以及部门领导短信汇报。  "></Step>
            <Step title="措施6" icon="md-trophy"" content=" 在航班保障的次日在民航局网站对统计有异议的航班进行申诉处理。 "></Step>
            <Step title="完成" icon="md-checkmark" status="finish" ></Step>
        </Steps>
        <br>
        <br>
        <Button type="primary" @click="Orange">措施检查</Button>
        <h2 style="line-height:70px;text-align: center">
            红色预警响应措施
        </h2>
        <Steps :current="currentr">
            <Step title="措施1" icon="ios-plane" content="对预警航班进行全面分析，主要包括航班结构、航班时刻、流量限制情况、天气情况等影响航班正常运行的因素。并指派专人（部门级别干部一人、区域经理一人）对该航班重点关注、分析，并给提高航班正常率的可行性方案，形成书面报告。 "></Step>
            <Step title="措施2" icon="ios-paper-plane" content="由部门牵头部门领导带队赴涉及该航班的相关管制单位、机场保障部门进行沟通协调。派出外站协调员赴当地管制单位进行协调工作。 "></Step>
            <Step title="措施3" icon="md-person-add" content="组织各生产保障部门召开运行协调会，根据航班分析报告结合各对部门保障要求形成预警航班保障方案。该保障方案需形成公司级文件下发至各部门以及各部门所联系的外委单位。 "></Step>
            <Step title="措施4" icon="ios-hammer" content="区域经理在值班过程中对预警航班以及涉及前序航班运行情况向运行总监以及部门领导短信汇报。 "></Step>
            <Step title="措施5" icon="md-trending-up" content="根据实际情况，为保障该航班正常可适当延误公司其他航班，区域经理应及时汇报公司值班经理、值班领导，并果断决策。  "></Step>
            <Step title="措施6" icon="md-trophy" content="在航班保障的次日在民航局网站对统计有异议的航班进行申诉处理。 "></Step>
            <Step title="措施7" icon="md-thumbs-up" content="负责该航班的部门级别干部以及区域经理应每周对该航班正常率、排名，以及该机场排名后10名的航班正常率排名进行分析，必要时可请示相关领导对航班进行计划性取消。 "></Step>
            <Step title="完成" icon="md-checkmark" status="finish" ></Step>
        </Steps>
        <br>
        <br>
        <Button type="primary" @click="Red">措施检查</Button>


    </i-col>
</template>

<script>
    export default {
        name: "Method"
    }
</script>

<style scoped>

</style>