import re
import json

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Replace Title
content = content.replace('<title>SBTI 人格测试</title>', '<title>《三角洲行动》干员招募评估</title>')

# Replace CSS
css_old = """    :root {
      --bg: #f6faf6;
      --panel: #ffffff;
      --text: #1e2a22;
      --muted: #6a786f;
      --line: #dbe8dd;
      --soft: #edf6ef;
      --accent: #6c8d71;
      --accent-strong: #4d6a53;
      --shadow: 0 16px 40px rgba(47, 73, 55, 0.08);
      --radius: 22px;
    }"""
css_new = """    :root {
      --bg: #0f1112;
      --panel: #1a1d1e;
      --text: #e2e8f0;
      --muted: #8b949e;
      --line: #2d3748;
      --soft: #23282b;
      --accent: #fbbf24;
      --accent-strong: #d97706;
      --shadow: 0 16px 40px rgba(0, 0, 0, 0.4);
      --radius: 12px;
    }"""
content = content.replace(css_old, css_new)

bg_old = """      background:
        radial-gradient(circle at top left, #f8fff8 0, #f6faf6 36%, #f2f7f3 100%);"""
bg_new = """      background:
        radial-gradient(circle at top left, #1c2124 0, #121415 36%, #0f1112 100%);"""
content = content.replace(bg_old, bg_new)

content = content.replace('linear-gradient(180deg, #fbfefb, #f3f8f4)', 'linear-gradient(180deg, #1a1d1e, #141617)')
content = content.replace('linear-gradient(180deg, #ffffff, #fbfdfb)', 'linear-gradient(180deg, #1a1d1e, #141617)')
content = content.replace('background: #fff;', 'background: #23282b;')
content = content.replace('background: #edf3ee;', 'background: #2d3748;')
content = content.replace('linear-gradient(90deg, #97b59c, #5b7a62)', 'linear-gradient(90deg, #fbbf24, #d97706)')
content = content.replace('color: #304034;', 'color: #e2e8f0;')

# Replace Hero HTML
hero_old = """<h1>MBTI已经过时，SBTI来了。</h1>"""
hero_new = """<h1>《三角洲行动》干员招募战术评估</h1>"""
content = content.replace(hero_old, hero_new)

hero_p_old = """        <div style="padding-top: 2rem; display: flex; flex-direction: column;">
          <span>
            原作者：
            <a href="https://space.bilibili.com/417038183">B站@蛆肉儿串儿</a>
          </span>
          <span>
            托管：Cloudflare (免费)
          </span>
          <span>
            域名：Spaceship (自费)
          </span>
        </div>"""
hero_p_new = """        <div style="padding-top: 2rem; display: flex; flex-direction: column; color: var(--muted);">
          <span>准备好加入特种部队了吗？完成以下战术决策评估，寻找最契合你的战斗定位。</span>
        </div>"""
content = content.replace(hero_p_old, hero_p_new)

# Generate new script part
script_new = """
    const dimensionMeta = {
      S1: { name: 'S1 战斗自信', model: '心理素质模型' },
      S2: { name: 'S2 战术清晰度', model: '心理素质模型' },
      S3: { name: 'S3 核心意志', model: '心理素质模型' },
      E1: { name: 'E1 后背交托', model: '团队信任度' },
      E2: { name: 'E2 团队羁绊', model: '团队信任度' },
      E3: { name: 'E3 独立与依赖', model: '团队信任度' },
      A1: { name: 'A1 敌意感知', model: '战场世界观' },
      A2: { name: 'A2 战术灵活性', model: '战场世界观' },
      A3: { name: 'A3 战斗意义', model: '战场世界观' },
      Ac1: { name: 'Ac1 进攻动机', model: '行动风格' },
      Ac2: { name: 'Ac2 决策速度', model: '行动风格' },
      Ac3: { name: 'Ac3 执行力度', model: '行动风格' },
      So1: { name: 'So1 战术主动性', model: '协同沟通' },
      So2: { name: 'So2 阵型边界感', model: '协同沟通' },
      So3: { name: 'So3 虚实与欺骗', model: '协同沟通' }
    };
    
    const questions = [
      { id: 'q1', dim: 'S1', text: '当小队在零号大坝遭遇突然的火力压制，你通常会：', options: [{label: '相信自己的枪法，寻找掩体反击', value: 3}, {label: '等待队长指示', value: 2}, {label: '优先撤退保命', value: 1}] },
      { id: 'q2', dim: 'S1', text: '你认为自己在团队中的战斗力：', options: [{label: '绝对的核心输出', value: 3}, {label: '稳定的中坚力量', value: 2}, {label: '更偏向辅助和掩护', value: 1}] },
      { id: 'q3', dim: 'S2', text: '在混乱的交火中，你能否迅速判断出敌方的火力分布？', options: [{label: '能立刻锁定敌人位置', value: 3}, {label: '需要时间观察', value: 2}, {label: '容易失去方向感', value: 1}] },
      { id: 'q4', dim: 'S2', text: '对于战术地图的记忆和运用，你：', options: [{label: '烂熟于心，随时规划路线', value: 3}, {label: '大概知道方位', value: 2}, {label: '基本跟着队友走', value: 1}] },
      { id: 'q5', dim: 'S3', text: '即使只剩你一个人，你也会坚持完成目标。', options: [{label: '不择手段也要赢', value: 3}, {label: '视情况而定', value: 2}, {label: '太危险了，选择撤退', value: 1}] },
      { id: 'q6', dim: 'S3', text: '在面对强敌时，你内心的波动：', options: [{label: '越战越勇，冷静如冰', value: 3}, {label: '有些紧张但能克制', value: 2}, {label: '压力极大，容易失误', value: 1}] },
      
      { id: 'q7', dim: 'E1', text: '在突进时，你敢把后背完全交给队友防守吗？', options: [{label: '完全信任，无需回头', value: 3}, {label: '会时不时确认一下', value: 2}, {label: '还是自己看着点更安心', value: 1}] },
      { id: 'q8', dim: 'E1', text: '队友报告说右侧安全，你会：', options: [{label: '直接忽略右侧专注前方', value: 3}, {label: '保持警惕', value: 2}, {label: '仍然会架枪防守右侧', value: 1}] },
      { id: 'q9', dim: 'E2', text: '如果队友倒在敌人的狙击视野内，你会：', options: [{label: '不顾一切去拉他', value: 3}, {label: '丢烟雾弹尝试营救', value: 2}, {label: '放弃他，避免葫芦娃救爷爷', value: 1}] },
      { id: 'q10', dim: 'E2', text: '你认为一支队伍获胜的关键是：', options: [{label: '兄弟同心其利断金', value: 3}, {label: '各司其职', value: 2}, {label: '个人英雄主义的发挥', value: 1}] },
      { id: 'q11', dim: 'E3', text: '你更喜欢怎样的战术站位？', options: [{label: '和队友紧密抱团', value: 1}, {label: '保持战术距离', value: 2}, {label: '单独拉枪线绕后', value: 3}] },
      { id: 'q12', dim: 'E3', text: '在执行侦察任务时，你：', options: [{label: '习惯单人行动', value: 3}, {label: '两人一组', value: 2}, {label: '全队一起推进', value: 1}] },
      
      { id: 'q13', dim: 'A1', text: '进入长弓溪谷的一个未探测建筑时，你会：', options: [{label: '假设每个角落都有敌人', value: 3}, {label: '保持警戒进入', value: 2}, {label: '大步流星走进去', value: 1}] },
      { id: 'q14', dim: 'A1', text: '听到微弱的脚步声，你会：', options: [{label: '立刻静步并架枪', value: 3}, {label: '通知队友', value: 2}, {label: '可能是自己听错了', value: 1}] },
      { id: 'q15', dim: 'A2', text: '原定计划是固守A点，但B点突然遭到猛攻，你会：', options: [{label: '果断放弃A点驰援B点', value: 3}, {label: '分兵支援', value: 2}, {label: '死守A点，服从命令', value: 1}] },
      { id: 'q16', dim: 'A2', text: '面对敌人的新型战术，你：', options: [{label: '能迅速找到破解之法', value: 3}, {label: '边打边想对策', value: 2}, {label: '按照传统经验应对', value: 1}] },
      { id: 'q17', dim: 'A3', text: '对你来说，一场战斗的意义在于：', options: [{label: '执行战术并获得胜利', value: 3}, {label: '体验交火的快感', value: 2}, {label: '收集高级物资和金钱', value: 1}] },
      { id: 'q18', dim: 'A3', text: '即使这局已经毫无胜算，你会：', options: [{label: '战斗到最后一刻', value: 3}, {label: '能杀一个是一个', value: 2}, {label: '直接放弃寻找撤离点', value: 1}] },
      
      { id: 'q19', dim: 'Ac1', text: '发现敌人踪迹后，你的第一反应是：', options: [{label: '直接开火压制', value: 3}, {label: '占据有利地形再打', value: 2}, {label: '隐蔽观察', value: 1}] },
      { id: 'q20', dim: 'Ac1', text: '在攻楼时，你通常：', options: [{label: '一马当先踹门而入', value: 3}, {label: '丢道具后跟进', value: 2}, {label: '在外面架枪掩护', value: 1}] },
      { id: 'q21', dim: 'Ac2', text: '面对岔路口，你决定路线的速度：', options: [{label: '一秒内拍板', value: 3}, {label: '稍微权衡利弊', value: 2}, {label: '犹豫不决，听别人的', value: 1}] },
      { id: 'q22', dim: 'Ac2', text: '当局势突变，你需要改变战术时：', options: [{label: '毫不犹豫切换模式', value: 3}, {label: '稍作停顿思考', value: 2}, {label: '容易卡壳不知所措', value: 1}] },
      { id: 'q23', dim: 'Ac3', text: '一旦制定了冲锋计划，你会：', options: [{label: '不顾一切冲到底', value: 3}, {label: '稳扎稳打推进', value: 2}, {label: '遇到阻力就退缩', value: 1}] },
      { id: 'q24', dim: 'Ac3', text: '在搜刮高价值区域时，你的动作：', options: [{label: '雷厉风行，绝不拖泥带水', value: 3}, {label: '仔细搜寻每一个角落', value: 2}, {label: '慢吞吞的容易磨叽', value: 1}] },
      
      { id: 'q25', dim: 'So1', text: '在小队语音中，你通常：', options: [{label: '不断报点，指挥全局', value: 3}, {label: '偶尔交流关键信息', value: 2}, {label: '基本闭麦，只听不说', value: 1}] },
      { id: 'q26', dim: 'So1', text: '遇到不认识的路人队友，你会：', options: [{label: '主动破冰，建立战术默契', value: 3}, {label: '看对方态度决定', value: 2}, {label: '各打各的，互不干扰', value: 1}] },
      { id: 'q27', dim: 'So2', text: '在阵地防守中，你：', options: [{label: '严格死守自己的防区', value: 3}, {label: '兼顾周围队友', value: 2}, {label: '到处乱跑', value: 1}] },
      { id: 'q28', dim: 'So2', text: '对于队友越界抢人头的行为，你：', options: [{label: '极其反感，破坏了战术阵型', value: 3}, {label: '只要能赢就行', value: 2}, {label: '觉得无所谓，自己也会这么干', value: 1}] },
      { id: 'q29', dim: 'So3', text: '在残局1v1时，你会：', options: [{label: '利用脚步声和道具欺骗对手', value: 3}, {label: '卡死角静待时机', value: 2}, {label: '直接拉出来对枪', value: 1}] },
      { id: 'q30', dim: 'So3', text: '面对敌方的试探性火力，你：', options: [{label: '故意不开枪，隐藏实力', value: 3}, {label: '反扔道具混淆视听', value: 2}, {label: '立刻还击暴露位置', value: 1}] }
    ];

    const specialQuestions = [
      {
        id: 'drink_gate_q1', special: true, kind: 'drink_gate',
        text: '在长弓溪谷执行任务时，你最看重的是什么？',
        options: [
          { label: '完成任务撤离', value: 1 },
          { label: '掩护队友', value: 2 },
          { label: '四处搜刮高价值物资', value: 3 },
          { label: '击败更多敌人', value: 4 }
        ]
      },
      {
        id: 'drink_gate_q2', special: true, kind: 'drink_trigger',
        text: '如果你在零号大坝发现了价值连城的“曼德尔砖”，但此时撤离点有重兵把守，你会：',
        options: [
          { label: '稳妥起见，放弃物资安全撤离', value: 1 },
          { label: '曼德尔砖！我的！谁挡我我杀谁！', value: 2 }
        ]
      }
    ];

    const TYPE_LIBRARY = {
      "Kai": { code: "红狼", cn: "凯·席尔瓦", intro: "动力外骨骼已就绪，准备突击！", desc: "你是天生的突击手。极高的战斗自信和进攻动机让你在战场上如鱼得水。你崇尚高机动的游击战术，往往能在对手反应过来之前就撕裂他们的防线。你不需要太多掩护，因为速度和爆发就是你最好的防御。" },
      "Terry": { code: "牧羊人", cn: "泰瑞·缪萨", intro: "防线已部署，你们背后交给我。", desc: "你是团队中最坚实的后盾。强烈的团队羁绊和稳重的决策让你成为不可或缺的工程兵。你擅长提前布防，化解敌方的每一波攻势。对于你来说，比起击杀敌人，确保队友的安全更具有战斗意义。" },
      "Luna": { code: "露娜", cn: "金卢娜", intro: "侦察箭矢已升空，猎物无处遁形。", desc: "你是战场上的信息掌控者。敏锐的敌意感知和战术清晰度让你总能快人一步。你习惯在行动前获取充足的情报，不打无准备之仗。你的存在就像是团队的“天眼”，让战术布置变得精准而致命。" },
      "Roy": { code: "蜂医", cn: "罗伊·斯米", intro: "别倒下，救援马上就到！", desc: "你是战场上最可靠的支援兵。极高的后背交托信任度和共情力让你始终关注着队友的状态。无论战况多么激烈，你都会优先保证团队的生存能力。有你在，队伍就拥有了源源不断的续航与希望。" },
      "Vyron": { code: "威龙", cn: "王宇昊", intro: "动能辅助开启，看我把他们轰上天！", desc: "你是破局的利刃。极强的执行力度和进攻动机让你敢于在最危险的时刻挺身而出。你善于利用火力优势瞬间压制敌人，在局部战场形成突破。你就是那颗随时准备引爆的磁吸炸弹，生猛且无畏。" },
      "Hackclaw": { code: "骇爪", cn: "麦晓雯", intro: "正在破译信号，敌方已成瞎子。", desc: "你是顶尖的电子攻防专家。战术灵活性和出色的欺骗技巧让你在战场上隐秘而致命。你不喜欢正面硬刚，更偏爱利用信息差和战术道具将敌人玩弄于股掌之间。你的每一次出手，都让对手防不胜防。" },
      "David": { code: "乌鲁鲁", cn: "大卫·费莱尔", intro: "掩体已就绪，火力压制开始！", desc: "你是战场上的移动堡垒。极高的战术心理素质和阵型边界感让你在面对任何火力时都能稳如泰山。你擅长利用掩体和重火力掌控战场节奏。只要你在，防线就永远不会崩溃。" },
      "MandelBrick": { code: "曼德尔砖", cn: "狂热淘金者", intro: "钱！全是我的钱！", desc: "你测出了本次测试的隐藏结果！在你的眼里，战术、团队、任务都是浮云，只有高价值物资才是真理。你是一个彻头彻尾的“仓鼠”玩家，只要看到保险箱和曼德尔砖，你的多巴胺就会疯狂分泌。小心别为了物资把命搭进去哦！" },
      "Runner": { code: "摸金校尉", cn: "跑刀仔", intro: "打仗是不可能打仗的，只能跑跑刀。", desc: "系统无法将你归入任何常规干员编制。你不仅游离于战术体系之外，甚至连基本的火力配备都没有。你可能只是一个拿着小刀、穿梭在战场边缘的跑刀仔，试图在混乱中捡点破烂。祝你好运，别被流弹刮到了！" }
    };

    const TYPE_IMAGES = {
      "Kai": "./image/delta_ops/Kai.png",
      "Terry": "./image/delta_ops/Terry.png",
      "Luna": "./image/delta_ops/Luna.png",
      "Roy": "./image/delta_ops/Roy.png",
      "Vyron": "./image/delta_ops/Vyron.png",
      "Hackclaw": "./image/delta_ops/Hackclaw.png",
      "David": "./image/delta_ops/David.png",
      "MandelBrick": "./image/delta_ops/MandelBrick.png",
      "Runner": "./image/delta_ops/MandelBrick.png"
    };

    const NORMAL_TYPES = [
      { code: "Kai", pattern: "HHH-MML-MHM-HHH-MML" },
      { code: "Terry", pattern: "MHM-HHM-HHH-MLM-LHM" },
      { code: "Luna", pattern: "HHL-MMH-HLM-MHL-HHH" },
      { code: "Roy", pattern: "MMH-HHH-MHL-LML-MHM" },
      { code: "Vyron", pattern: "HHM-MHL-LHM-HHH-LHL" },
      { code: "Hackclaw", pattern: "HHL-LHM-HLM-MHL-HHH" },
      { code: "David", pattern: "HHL-HMM-LHH-MML-HLH" }
    ];

    const DIM_EXPLANATIONS = {
      "S1": { "L": "战斗自信偏低，偏向保守。", "M": "正常发挥，视情况而定。", "H": "自信心爆棚，敢打敢拼。" },
      "S2": { "L": "战术意识较弱，容易迷失方向。", "M": "有一定的战术素养，能跟上节奏。", "H": "战术清晰度极高，全局掌控者。" },
      "S3": { "L": "意志容易动摇，遇到挫折想撤退。", "M": "能够坚持，但也有妥协的时候。", "H": "核心意志坚如磐石，绝不退缩。" },
      "E1": { "L": "习惯单打独斗，防备心重。", "M": "信任队友，但保留一丝警惕。", "H": "完全信任，后背放心交给队友。" },
      "E2": { "L": "团队羁绊较弱，各自为战。", "M": "有团队意识，愿意配合。", "H": "极度看重团队，愿意为队友牺牲。" },
      "E3": { "L": "喜欢抱团，依赖队友掩护。", "M": "能独立作战也能配合。", "H": "高度独立，习惯单兵作战绕后。" },
      "A1": { "L": "神经大条，对危险不敏感。", "M": "保持正常警惕。", "H": "草木皆兵，极高的敌意感知。" },
      "A2": { "L": "思维固化，认死理。", "M": "能根据情况做出调整。", "H": "战术极其灵活，不拘一格。" },
      "A3": { "L": "只在乎个人利益或物资。", "M": "体验过程，享受游戏。", "H": "把胜利和战术执行看作最高目标。" },
      "Ac1": { "L": "偏好防守，不爱主动出击。", "M": "攻守平衡。", "H": "进攻欲望极强，永远冲在最前。" },
      "Ac2": { "L": "决策容易犹豫，错失良机。", "M": "思考后做出合理决策。", "H": "决策极快，雷厉风行。" },
      "Ac3": { "L": "执行力较弱，容易拖沓。", "M": "正常执行任务。", "H": "不打折扣地完成目标，执行力爆表。" },
      "So1": { "L": "基本不交流，闭麦玩家。", "M": "必要时进行沟通。", "H": "战术指挥家，沟通积极主动。" },
      "So2": { "L": "没有边界感，容易乱跑乱抢。", "M": "有基本的防区意识。", "H": "严格遵守战术边界和纪律。" },
      "So3": { "L": "直来直去，容易被套路。", "M": "有一定的防骗意识。", "H": "战术欺骗大师，心眼子极多。" }
    };
"""

# Now replace the script part from `const dimensionMeta` up to `const dimensionOrder`
script_pattern = re.compile(r'const dimensionMeta = \{.*?\n    const dimensionOrder =', re.DOTALL)
content = script_pattern.sub(script_new.strip() + '\n    const dimensionOrder =', content)

# Change TYPE_LIBRARY.DRUNK and TYPE_LIBRARY.HHHH in logic
content = content.replace('TYPE_LIBRARY.DRUNK', 'TYPE_LIBRARY.MandelBrick')
content = content.replace('TYPE_LIBRARY.HHHH', 'TYPE_LIBRARY.Runner')

# Change author box
author_old = """              <p>本测试首发于b站up主蛆肉儿串儿（UID417038183），初衷是劝诫一位爱喝酒的朋友戒酒。</p>
              <p>由于作者的人格是SHIT愤世者，所以平等的攻击了各位，在此抱歉！！不过我是一个绝世大美女，你们一定会原谅我，有B站的朋友们也可以关注我。</p>
              <p>关于这个测试，我没法很好的平衡娱乐和专业性，因此对于一些人格的阐释较为模糊或完全不准（如屌丝可能并非真的屌丝），如有冒犯非常抱歉！！</p>
              <p>再鉴于时间精力有限，就随便搞了一个先这样玩玩，后续会慢慢完善修改的，总之好玩为主，还请不要用于盈利呀。</p>"""
author_new = """              <p>本测试基于《三角洲行动》干员设定进行战术向改编。</p>
              <p>通过15个战术维度的评估，为您寻找最契合的战斗定位和本命干员。</p>
              <p>题目仅供娱乐，如果在测试中测出了“曼德尔砖”或者“摸金校尉”，请不要怀疑，你就是长弓溪谷里最亮的仔。</p>"""
content = content.replace(author_old, author_new)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)

