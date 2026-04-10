import re

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Define the new script block containing questions, TYPE_LIBRARY, TYPE_IMAGES, NORMAL_TYPES
new_script = """
    const dimensionMeta = {
      S1: { name: 'S1 战斗自信', model: '战术心理素质' },
      S2: { name: 'S2 战术清晰度', model: '战术心理素质' },
      S3: { name: 'S3 核心意志', model: '战术心理素质' },
      E1: { name: 'E1 后背交托', model: '团队信任度' },
      E2: { name: 'E2 团队羁绊', model: '团队信任度' },
      E3: { name: 'E3 独立与依赖', model: '团队信任度' },
      A1: { name: 'A1 敌意感知', model: '战场世界观' },
      A2: { name: 'A2 战术灵活性', model: '战场世界观' },
      A3: { name: 'A3 战斗意义', model: '战场世界观' },
      Ac1: { name: 'Ac1 进攻动机', model: '行动风格' },
      Ac2: { name: 'Ac2 决策速度', model: '行动风格' },
      Ac3: { name: 'Ac3 执行力度', model: '行动风格' },
      So1: { name: 'So1 战术主动性', model: '协同与沟通' },
      So2: { name: 'So2 阵型边界感', model: '协同与沟通' },
      So3: { name: 'So3 虚实与欺骗', model: '协同与沟通' }
    };

    const questions = [
      // S1 战斗自信
      { id: 'q1', dim: 'S1', text: '零号大坝局势逆风，队友全倒，你手捏一把白板MP5，你会：', options: [{label: '“我就是奇迹！”直接冲出去一穿四', value: 3}, {label: '“能杀一个不亏”，找个掩体架枪等有缘人', value: 2}, {label: '“这把坐牢了”，默默丢掉装备找撤离点', value: 1}] },
      { id: 'q2', dim: 'S1', text: '路人队友开局就嘲讽你“段位太低”，你的反应是：', options: [{label: '“等下看我战绩说话，让你叫爹”', value: 3}, {label: '不理他，自己打自己的', value: 2}, {label: '有点慌，生怕自己待会真的坑了', value: 1}] },
      // S2 战术清晰度
      { id: 'q3', dim: 'S2', text: '刚进航天基地，四面八方都是枪声，你的大脑状态：', options: [{label: '瞬间脑补出三支队伍的位置和火拼情况', value: 3}, {label: '大概知道哪边人多，决定绕着走', value: 2}, {label: '“我在哪？谁在打我？我该往哪跑？”', value: 1}] },
      { id: 'q4', dim: 'S2', text: '你对长弓溪谷地图的熟悉程度堪称：', options: [{label: '“连哪块石头后面能蹲老六我都门儿清”', value: 3}, {label: '“大点位认得，野区偶尔迷路”', value: 2}, {label: '“跟着队友走，队友去哪我去哪”', value: 1}] },
      // S3 核心意志
      { id: 'q5', dim: 'S3', text: '你千辛万苦摸到一把满改大狙，突然被冷枪打成大残，你会：', options: [{label: '“敢动我的枪？今天你必须死！”打满药回去复仇', value: 3}, {label: '看情况，有机会就打，没机会就溜', value: 2}, {label: '“枪没了可以再买，命没了就全白给了”，赶紧跑', value: 1}] },
      { id: 'q6', dim: 'S3', text: '连续五把“落地成盒”，此时你的心态：', options: [{label: '“我就不信了，下一把把把C！”立马开', value: 3}, {label: '深吸一口气，换个打法或者换张图', value: 2}, {label: '“这游戏针对我”，光速下线', value: 1}] },
      // E1 后背交托
      { id: 'q7', dim: 'E1', text: '你正在激情对枪，队友说“你背后我架住了”，你会：', options: [{label: '完全无视背后，死磕正面', value: 3}, {label: '正面打两枪，余光瞥一眼背后', value: 2}, {label: '“我不信”，时不时回头看一眼才安心', value: 1}] },
      { id: 'q8', dim: 'E1', text: '你和野排队友一起搜刮高级物资区，你的防备心：', options: [{label: '“都是兄弟，随便搜”', value: 3}, {label: '一人搜一边，互不干涉', value: 2}, {label: '“防人之心不可无，别抢我红卡”', value: 1}] },
      // E2 团队羁绊
      { id: 'q9', dim: 'E2', text: '你的好基友倒在了敌人的大狙枪口下，周围毫无掩体，你会：', options: [{label: '“兄弟我来了！”捏着烟雾弹强行去拉', value: 3}, {label: '先想办法把对面大狙逼退，再找机会救', value: 2}, {label: '“兄弟你安心去吧，你的物资我帮你带出来”', value: 1}] },
      { id: 'q10', dim: 'E2', text: '一局游戏结束，你发现自己数据很差，但队伍赢了，你会：', options: [{label: '“只要赢了就行，我就是团队最强后盾”', value: 3}, {label: '还行吧，躺赢也算赢', value: 2}, {label: '“毫无体验，这把玩得太憋屈了”', value: 1}] },
      // E3 独立与依赖
      { id: 'q11', dim: 'E3', text: '在战术分配时，你最倾向的位置是：', options: [{label: '“我去单带绕后，你们正面吸引火力”', value: 3}, {label: '“我和老王走侧翼包抄”', value: 2}, {label: '“大家抱紧一点，千万别散开了”', value: 1}] },
      { id: 'q12', dim: 'E3', text: '当你落单面对敌方满编队时，你的第一反应是：', options: [{label: '“一打四？优势在我！”', value: 3}, {label: '“尽量多换几个，不亏”', value: 2}, {label: '“呼叫支援！快来救驾！”', value: 1}] },
      // A1 敌意感知
      { id: 'q13', dim: 'A1', text: '路过一片安静得出奇的建筑群，你的直觉告诉你：', options: [{label: '“安静得可怕，绝对有老六，全体戒备”', value: 3}, {label: '“小心点，随时准备交火”', value: 2}, {label: '“没人来过，赶紧进去搜刮”', value: 1}] },
      { id: 'q14', dim: 'A1', text: '听到远处传来细微的踩草声，你的操作是：', options: [{label: '秒蹲下，切出满改步枪，屏息凝神', value: 3}, {label: '停下脚步，向队友报点', value: 2}, {label: '“风声吧？或者是远处的枪声”，继续走', value: 1}] },
      // A2 战术灵活性
      { id: 'q15', dim: 'A2', text: '原计划是守株待兔，结果敌人完全不按套路出牌从背后摸上来了，你会：', options: [{label: '“来得好！”瞬间放弃原计划，反包围他们', value: 3}, {label: '边打边撤，寻找新的防守点', value: 2}, {label: '“怎么不按剧本走啊”，一时手忙脚乱', value: 1}] },
      { id: 'q16', dim: 'A2', text: '面对敌方的新型战术（比如全是无人机和毒气），你的应对：', options: [{label: '“有意思，看我用奇招破你”', value: 3}, {label: '观察一波，看看队友怎么打', value: 2}, {label: '“这怎么玩？根本没法打啊”', value: 1}] },
      // A3 战斗意义
      { id: 'q17', dim: 'A3', text: '对你来说，三角洲最让你爽的瞬间是：', options: [{label: '“极限翻盘，战术执行完美的瞬间”', value: 3}, {label: '“和队友打出完美配合，欢声笑语”', value: 2}, {label: '“开出大金，一夜暴富的瞬间”', value: 1}] },
      { id: 'q18', dim: 'A3', text: '如果一局游戏你啥也没干，光跟着跑图就撤离了，你会觉得：', options: [{label: '“太无聊了，这是在浪费生命”', value: 3}, {label: '“当个跑酷模拟器也不错”', value: 2}, {label: '“兵不血刃，白嫖物资，血赚！”', value: 1}] },
      // Ac1 进攻动机
      { id: 'q19', dim: 'Ac1', text: '确认前方房区有一队人正在搜东西，你的指示是：', options: [{label: '“全军出击！给我把门踹开！”', value: 3}, {label: '“先扔雷，封走位，再慢慢清”', value: 2}, {label: '“别开枪，等他们出来打个背身，或者直接溜”', value: 1}] },
      { id: 'q20', dim: 'Ac1', text: '听到枪声，你的脚指头会：', options: [{label: '不自觉地往枪声方向挪动，根本控不住想劝架的心', value: 3}, {label: '先看地图，判断距离和地形再决定去不去', value: 2}, {label: '立刻反向逃跑，远离是非之地', value: 1}] },
      // Ac2 决策速度
      { id: 'q21', dim: 'Ac2', text: '遇到岔路口，左边可能有埋伏，右边路远但安全，你决定：', options: [{label: '“一秒钟决定，走哪边都行，别墨迹”', value: 3}, {label: '“权衡一下利弊，大概十秒钟给出方案”', value: 2}, {label: '“你们定吧，我选择困难症犯了”', value: 1}] },
      { id: 'q22', dim: 'Ac2', text: '当看到红卡房门被打开的一瞬间，你的反应速度：', options: [{label: '肌肉记忆已经开枪了', value: 3}, {label: '大脑飞速运转，寻找掩体', value: 2}, {label: '“啊？开了？谁开的？”', value: 1}] },
      // Ac3 执行力度
      { id: 'q23', dim: 'Ac3', text: '一旦决定了要冲一波，你会：', options: [{label: '“油门踩到底，不撞南墙不回头”', value: 3}, {label: '“见机行事，不对劲就撤”', value: 2}, {label: '“冲到一半突然有点怂了，想退回来”', value: 1}] },
      { id: 'q24', dim: 'Ac3', text: '在执行搜刮指令时，你的动作是：', options: [{label: '“风卷残云，三秒钟清空一个房间”', value: 3}, {label: '“仔细检查，不放过任何一个角落”', value: 2}, {label: '“搜着搜着就不知道该干嘛了，发呆”', value: 1}] },
      // So1 战术主动性
      { id: 'q25', dim: 'So1', text: '在随机匹配的队伍里，你的麦克风状态：', options: [{label: '“指挥官附体，疯狂报点布置战术”', value: 3}, {label: '“有人说话我就搭理，没人说我就闭麦”', value: 2}, {label: '“从不开麦，做一个安静的美男子/美少女”', value: 1}] },
      { id: 'q26', dim: 'So1', text: '遇到沉默寡言的路人队友，你会：', options: [{label: '“强行破冰，活跃气氛，疯狂丢道具逗他”', value: 3}, {label: '“正常交流关键信息，不强求”', value: 2}, {label: '“他不说我也不说，大家比比谁更能憋”', value: 1}] },
      // So2 阵型边界感
      { id: 'q27', dim: 'So2', text: '防守据点时，队友老是乱跑出防区，你会：', options: [{label: '“开麦怒喷，让他赶紧滚回来守点”', value: 3}, {label: '“提醒他注意安全，自己帮他补位”', value: 2}, {label: '“管他呢，他死了正好我可以捡他装备”', value: 1}] },
      { id: 'q28', dim: 'So2', text: '对于“越界抢人头”这种行为，你的看法：', options: [{label: '“极其反感，破坏了完美的战术阵型！”', value: 3}, {label: '“只要能赢，谁杀都一样”', value: 2}, {label: '“抢人头就是快乐，我自己也天天抢”', value: 1}] },
      // So3 虚实与欺骗
      { id: 'q29', dim: 'So3', text: '残局1v1，你最喜欢的套路是：', options: [{label: '“各种假脚步、丢烟雾弹迷惑，把他绕晕再背刺”', value: 3}, {label: '“找个刁钻的角度架枪，等他上钩”', value: 2}, {label: '“拼了！直接拉出去干拉对枪！”', value: 1}] },
      { id: 'q30', dim: 'So3', text: '面对敌人的试探性开火，你会：', options: [{label: '“假装没人在，等他完全放松警惕再一网打尽”', value: 3}, {label: '“扔个手雷回去警告一下”', value: 2}, {label: '“敢打我？立刻火力全开还击暴露位置”', value: 1}] }
    ];

    const specialQuestions = [
      {
        id: 'drink_gate_q1', special: true, kind: 'drink_gate',
        text: '在长弓溪谷，前方是撤离点，脚下是一个极品保险箱，但周围可能有埋伏，你选择：',
        options: [
          { label: '命最重要，直接跑路撤离', value: 1 },
          { label: '兄弟们架枪，我来摸', value: 2 },
          { label: '保险箱！就算被六我也要摸！', value: 3 },
          { label: '我不摸箱子，我专门蹲在箱子旁边阴那些来摸箱子的人', value: 4 }
        ]
      },
      {
        id: 'drink_gate_q2', special: true, kind: 'drink_trigger',
        text: '当你看到“曼德尔砖”四个字时，你的第一反应是：',
        options: [
          { label: '高价值物资，值得冒险，但也要谨慎', value: 1 },
          { label: '曼德尔砖！全是我的！谁挡我我杀谁！', value: 2 }
        ]
      }
    ];

    const TYPE_LIBRARY = {
      // 官方干员 1-14
      "Kai": { code: "红狼", cn: "凯·席尔瓦", intro: "动力外骨骼已就绪，准备突击！", desc: "你是天生的突击手。极高的战斗自信和进攻动机让你在战场上如鱼得水。你崇尚高机动的游击战术，往往能在对手反应过来之前就撕裂他们的防线。你不需要太多掩护，因为速度和爆发就是你最好的防御。" },
      "Terry": { code: "牧羊人", cn: "泰瑞·缪萨", intro: "防线已部署，你们背后交给我。", desc: "你是团队中最坚实的后盾。强烈的团队羁绊和稳重的决策让你成为不可或缺的工程兵。你擅长提前布防，化解敌方的每一波攻势。对于你来说，比起击杀敌人，确保队友的安全更具有战斗意义。" },
      "Luna": { code: "露娜", cn: "金卢娜", intro: "侦察箭矢已升空，猎物无处遁形。", desc: "你是战场上的信息掌控者。敏锐的敌意感知和战术清晰度让你总能快人一步。你习惯在行动前获取充足的情报，不打无准备之仗。你的存在就像是团队的“天眼”，让战术布置变得精准而致命。" },
      "Roy": { code: "蜂医", cn: "罗伊·斯米", intro: "别倒下，救援马上就到！", desc: "你是战场上最可靠的支援兵。极高的后背交托信任度和共情力让你始终关注着队友的状态。无论战况多么激烈，你都会优先保证团队的生存能力。有你在，队伍就拥有了源源不断的续航与希望。" },
      "Vyron": { code: "威龙", cn: "王宇昊", intro: "动能辅助开启，看我把他们轰上天！", desc: "你是破局的利刃。极强的执行力度和进攻动机让你敢于在最危险的时刻挺身而出。你善于利用火力优势瞬间压制敌人，在局部战场形成突破。你就是那颗随时准备引爆的磁吸炸弹，生猛且无畏。" },
      "Hackclaw": { code: "骇爪", cn: "麦晓雯", intro: "正在破译信号，敌方已成瞎子。", desc: "你是顶尖的电子攻防专家。战术灵活性和出色的欺骗技巧让你在战场上隐秘而致命。你不喜欢正面硬刚，更偏爱利用信息差和战术道具将敌人玩弄于股掌之间。你的每一次出手，都让对手防不胜防。" },
      "David": { code: "乌鲁鲁", cn: "大卫·费莱尔", intro: "掩体已就绪，火力压制开始！", desc: "你是战场上的移动堡垒。极高的战术心理素质和阵型边界感让你在面对任何火力时都能稳如泰山。你擅长利用掩体和重火力掌控战场节奏。只要你在，防线就永远不会崩溃。" },
      "SilverWing": { code: "银翼", cn: "兰登·穆勒", intro: "猎鹰已升空，目标已锁定。", desc: "你是战场上的幽灵眼。超强的追踪索敌能力和情报收集让你总能掌握敌人的蛛丝马迹。你喜欢在暗处观察，利用无人机和脉冲手雷瘫痪敌方的电子设备，将一切尽在掌握。" },
      "Butterfly": { code: "蝶", cn: "莉娜·范德梅尔", intro: "无人机已就位，准备医疗支援。", desc: "你是团队的守护天使。无人机医疗和远程补给是你的拿手好戏。你不需要冲锋陷阵，只要你在后方，队友就拥有了源源不断的生命力，是小队不可或缺的生存保障。" },
      "Bit": { code: "比特", cn: "拉希德·拉哈尔", intro: "智能陷阱已部署，小心脚下。", desc: "你是机械操控大师。智能烟雾地雷和哨兵母巢是你控场的利器。你善于利用各种高科技机械来限制敌人的行动，让敌人在你的科技迷宫中寸步难行。" },
      "Zoya": { code: "佐娅", cn: "蛊", intro: "激素已注入，准备迎接毒雾吧。", desc: "你是战场上的化学家。激素增益和致盲毒雾让你在辅助和控制之间游刃有余。你不仅能让队友变得更强，还能让敌人在毒雾中迷失方向，是极其难缠的对手。" },
      "DeepBlue": { code: "深蓝", cn: "阿列克谢·彼得罗夫", intro: "防爆盾展开，跟我冲！", desc: "你是坚不可摧的重装先锋。防爆盾推进和多功能钩爪枪让你攻防一体。你习惯顶在队伍最前面吸收伤害，同时用钩爪给敌人致命一击，是名副其实的“盾狗”。" },
      "Nameless": { code: "无名", cn: "Nameless", intro: "阴影之中，取你首级。", desc: "你是致命的暗影刺客。静默潜袭和闪光突进是你的成名绝技。你最擅长反侦察和绕后暗杀，常常在敌人还未反应过来时就已完成收割，是所有脆皮的梦魇。" },
      "AsaraGuard": { code: "阿萨拉卫士", cn: "Asara Guard", intro: "坚守阵地，绝不退缩！", desc: "你是忠诚的阿萨拉卫士。虽然只是NPC阵营的一员，但你的意志坚如磐石。你不屈不挠地坚守着自己的阵地，用猛烈的火力回击一切入侵者，令人敬畏。" },
      // 热梗彩蛋 15-27
      "MandelBrick": { code: "曼德尔砖", cn: "狂热淘金者", intro: "钱！全是我的钱！", desc: "你测出了本次测试的隐藏结果！在你的眼里，战术、团队、任务都是浮云，只有高价值物资才是真理。你是一个彻头彻尾的“仓鼠”玩家，只要看到保险箱和曼德尔砖，你的多巴胺就会疯狂分泌。小心别为了物资把命搭进去哦！" },
      "Runner": { code: "摸金校尉", cn: "跑刀仔", intro: "打仗是不可能打仗的，只能跑跑刀。", desc: "系统无法将你归入任何常规干员编制。你不仅游离于战术体系之外，甚至连基本的火力配备都没有。你可能只是一个拿着小刀、穿梭在战场边缘的跑刀仔，试图在混乱中捡点破烂。祝你好运，别被流弹刮到了！" },
      "AfricanStar": { code: "非洲之星", cn: "African Star", intro: "又是一把白板...我的大金呢？", desc: "你测出了极其罕见的非酋体质！不管多高级的箱子，你摸出来永远是一堆破烂。你的运气差到了极点，建议以后搜刮物资这种事还是交给队友吧，你只负责打架就行了。" },
      "TearOfOcean": { code: "海洋之泪", cn: "欧皇本皇", intro: "随便摸一下就是天价物资，哎，无敌是多么寂寞。", desc: "你是万中无一的欧皇！你的运气好到离谱，随便打开一个垃圾桶都能摸出大金。队友都把你当成吉祥物供着，你是名副其实的“人形自走摸金机器”。" },
      "T6Juggernaut": { code: "六套战神", cn: "T6 Juggernaut", intro: "全身六套，莽就完事了！", desc: "你是名副其实的“氪金玩家”。全身最顶级的装备让你无所畏惧，你信奉“用金钱碾压一切”的战术。不需要什么花里胡哨的操作，站着让你打你都打不死我，这就是六套战神的底气！" },
      "DamGuard": { code: "大坝保安", cn: "Dam Guard", intro: "零号大坝，我的地盘我做主。", desc: "你是零号大坝的常驻保安。你对大坝的每一个角落、每一个地堡都了如指掌。你最喜欢在复杂的房区里和敌人捉迷藏，你是这片钢筋水泥森林里真正的“地头蛇”。" },
      "LongbowSniper": { code: "长弓狙神", cn: "伏地魔", intro: "只要我不动，就没有人能发现我。", desc: "你是极度耐心的狙击手。你可以在长弓溪谷的山顶上趴一整局一动不动，只为了那致命的一击。千里之外取人首级是你的浪漫，你是战场上最让人头疼的“伏地魔”。" },
      "SpaceRat": { code: "航天仓鼠", cn: "Space Rat", intro: "只要背包没满，我就还要搜！", desc: "你是航天基地的资深“仓鼠”。你专挑那些犄角旮旯的地方躲着，偷偷把背包塞得满满当当。打架？不存在的，你的眼里只有物资和撤离点。" },
      "ToeClipper": { code: "修脚大师", cn: "Toe Clipper", intro: "护甲再厚，腿也是脆的！", desc: "你是让所有重装干员闻风丧胆的“修脚大师”。你深知打高护甲的敌人毫无意义，于是你苦练喷子和冲锋枪，专打敌人护甲覆盖不到的腿部。几枪下去，六套也得跪下唱征服。" },
      "OutlineMaster": { code: "描边大师", cn: "Outline Master", intro: "一顿操作猛如虎，一看伤害二十五。", desc: "你的枪法简直是“艺术”。你能在极近的距离内完美避开敌人的身体，在他们周围打出一圈完美的弹孔轮廓。你的队友常常看着你的操作陷入沉思：你到底是在打人还是在画画？" },
      "MedicsDaddy": { code: "医疗兵的爹", cn: "Medic's Daddy", intro: "蜂医救我！我又要倒了！", desc: "你是队伍里最不安分的因素。你总是疯狂冲锋，然后疯狂倒地，全场都在回荡着你喊“救命”的声音。你凭一己之力拉高了队伍里医疗兵的血压，是当之无愧的“医疗兵亲爹”。" },
      "GrenadeGod": { code: "雷神", cn: "Grenade God", intro: "艺术就是爆炸！", desc: "你是战场上的爆破狂。你的包里装满了各种手雷、燃烧弹和烟雾弹。你不喜欢对枪，你更喜欢用漫天的投掷物覆盖整个战场，让敌人在爆炸和火海中绝望挣扎。" },
      "TheRat": { code: "老六", cn: "The Rat", intro: "只要我不出声，我就是隐形的。", desc: "你是极度阴险的战术家，也就是俗称的“老六”。你永远躲在门后、草丛里或者黑暗的角落，静静等待猎物上钩。你的存在让所有玩家在搜点时都心惊胆战，生怕转角遇到爱。" }
    };

    const TYPE_IMAGES = {
      "Kai": "./image/delta_ops/Kai.png",
      "Terry": "./image/delta_ops/Terry.png",
      "Luna": "./image/delta_ops/Luna.png",
      "Roy": "./image/delta_ops/Roy.png",
      "Vyron": "./image/delta_ops/Vyron.png",
      "Hackclaw": "./image/delta_ops/Hackclaw.png",
      "David": "./image/delta_ops/David.png",
      "SilverWing": "./image/delta_ops/SilverWing.jpg",
      "Butterfly": "./image/delta_ops/Butterfly.jpg",
      "Bit": "./image/delta_ops/Bit.jpg",
      "Zoya": "./image/delta_ops/Zoya.jpg",
      "DeepBlue": "./image/delta_ops/DeepBlue.jpg",
      "Nameless": "./image/delta_ops/Nameless.jpg",
      "AsaraGuard": "./image/delta_ops/AsaraGuard.jpg",
      "MandelBrick": "./image/delta_ops/MandelBrick.png",
      "Runner": "./image/delta_ops/Runner.png",
      "AfricanStar": "./image/delta_ops/AfricanStar.jpg",
      "TearOfOcean": "./image/delta_ops/TearOfOcean.jpg",
      "T6Juggernaut": "./image/delta_ops/T6Juggernaut.jpg",
      "DamGuard": "./image/delta_ops/DamGuard.jpg",
      "LongbowSniper": "./image/delta_ops/LongbowSniper.jpg",
      "SpaceRat": "./image/delta_ops/SpaceRat.jpg",
      "ToeClipper": "./image/delta_ops/ToeClipper.jpg",
      "OutlineMaster": "./image/delta_ops/OutlineMaster.jpg",
      "MedicsDaddy": "./image/delta_ops/MedicsDaddy.jpg",
      "GrenadeGod": "./image/delta_ops/GrenadeGod.jpg",
      "TheRat": "./image/delta_ops/TheRat.jpg"
    };

    // 分配25个常规匹配向量，映射到25个人格（不含酒鬼触发和兜底的2个）
    const NORMAL_TYPES = [
      { code: "Kai", pattern: "HHH-MML-MHM-HHH-MML" },
      { code: "Terry", pattern: "MHM-HHM-HHH-MLM-LHM" },
      { code: "Luna", pattern: "HHL-MMH-HLM-MHL-HHH" },
      { code: "Roy", pattern: "MMH-HHH-MHL-LML-MHM" },
      { code: "Vyron", pattern: "HHM-MHL-LHM-HHH-LHL" },
      { code: "Hackclaw", pattern: "HHL-LHM-HLM-MHL-HHH" },
      { code: "David", pattern: "HHL-HMM-LHH-MML-HLH" },
      { code: "SilverWing", pattern: "HML-LHM-HLH-MHM-HHM" },
      { code: "Butterfly", pattern: "LMM-HHM-MHM-LMM-MHM" },
      { code: "Bit", pattern: "MHL-MHM-HHM-MML-HHM" },
      { code: "Zoya", pattern: "MHM-HMM-HHL-MLM-HLH" },
      { code: "DeepBlue", pattern: "HHM-HHH-MHL-HMM-MHM" },
      { code: "Nameless", pattern: "HHH-LLH-HLM-HHH-LHH" },
      { code: "AsaraGuard", pattern: "MMH-MHM-HHM-MHM-LHM" },
      { code: "AfricanStar", pattern: "LLL-LLL-LHL-LLL-LLL" },
      { code: "TearOfOcean", pattern: "HHH-LLL-LHL-MML-LLL" },
      { code: "T6Juggernaut", pattern: "HHH-LLM-HHL-HHH-LLL" },
      { code: "DamGuard", pattern: "MHM-MHM-HHL-MHM-HHM" },
      { code: "LongbowSniper", pattern: "HHL-LHM-HLM-LLL-HHH" },
      { code: "SpaceRat", pattern: "LML-MML-LHH-LLL-LLL" },
      { code: "ToeClipper", pattern: "HHL-LML-HHL-HHM-LML" },
      { code: "OutlineMaster", pattern: "HHH-LLL-HHL-HHH-LML" },
      { code: "MedicsDaddy", pattern: "HHH-HHL-LHL-HHH-LLL" },
      { code: "GrenadeGod", pattern: "MHL-LHM-HHL-MHL-MHM" },
      { code: "TheRat", pattern: "HHL-LHM-HHL-LLL-HHH" }
    ];

    const DIM_EXPLANATIONS = {
      "S1": { "L": "战斗自信偏低，看到人先怂一半，常年被压制。", "M": "正常发挥，顺风如狼，逆风如鼠。", "H": "自信心爆棚，敢打敢拼，眼里没有“撤退”二字。" },
      "S2": { "L": "战术意识较弱，容易迷失方向，我是谁我在哪？", "M": "有一定的战术素养，能跟上队伍的节奏。", "H": "战术清晰度极高，战场全局掌控者，人称小雷达。" },
      "S3": { "L": "意志容易动摇，遇到挫折就想跑路保命。", "M": "能够坚持，但遇到硬茬也有妥协的时候。", "H": "核心意志坚如磐石，为了目标绝不退缩。" },
      "E1": { "L": "习惯单打独斗，防备心极重，谁都不信。", "M": "信任队友，但保留一丝警惕，偶尔回头看一眼。", "H": "完全信任，把后背放心交给队友，闭着眼往前冲。" },
      "E2": { "L": "团队羁绊较弱，各自为战，大难临头各自飞。", "M": "有团队意识，愿意配合，必要时会伸出援手。", "H": "极度看重团队，愿意为队友牺牲，甚至肉身挡子弹。" },
      "E3": { "L": "喜欢抱团，极度依赖队友掩护，一个人不敢走。", "M": "能独立作战也能配合，弹性极强。", "H": "高度独立，习惯单兵作战绕后，独狼玩家。" },
      "A1": { "L": "神经大条，对危险毫不敏感，经常大摇大摆送人头。", "M": "保持正常警惕，遇到异响会停下观察。", "H": "草木皆兵，极高的敌意感知，总觉得有人在阴自己。" },
      "A2": { "L": "思维固化，认死理，一条路走到黑。", "M": "能根据情况做出调整，有一定的应变能力。", "H": "战术极其灵活，不拘一格，满脑子都是骚套路。" },
      "A3": { "L": "只在乎个人利益或物资，打仗哪有摸金香？", "M": "体验过程，享受游戏，输赢不重要，开心就好。", "H": "把胜利和战术执行看作最高目标，纯粹的战争机器。" },
      "Ac1": { "L": "偏好防守，绝不主动出击，能苟就苟。", "M": "攻守平衡，看准时机才会动手。", "H": "进攻欲望极强，永远冲在最前面，见面就是干。" },
      "Ac2": { "L": "决策极度犹豫，错失良机，脑内会议常年超时。", "M": "思考后做出合理决策，中规中矩。", "H": "决策极快，雷厉风行，一秒钟拍板绝不墨迹。" },
      "Ac3": { "L": "执行力较弱，容易拖沓，搜东西磨磨唧唧。", "M": "正常执行任务，不快也不慢。", "H": "不打折扣地完成目标，执行力爆表，风卷残云。" },
      "So1": { "L": "基本不交流，万年闭麦玩家，纯靠意念沟通。", "M": "必要时开麦报点，平时保持安静。", "H": "战术指挥家，沟通积极主动，语音频道永远有他的声音。" },
      "So2": { "L": "毫无边界感，到处乱跑乱抢，经常干扰队友。", "M": "有基本的防区意识，知道自己该干嘛。", "H": "严格遵守战术边界和纪律，死守阵地绝不越界。" },
      "So3": { "L": "直来直去，纯粹的铁憨憨，经常被各种套路玩弄。", "M": "有一定的防骗意识，偶尔也会耍点小聪明。", "H": "战术欺骗大师，心眼子极多，全身都是假动作。" }
    };
"""

script_pattern = re.compile(r'const dimensionMeta = \{.*?\n    const dimensionOrder =', re.DOTALL)
content = script_pattern.sub(new_script.strip() + '\n    const dimensionOrder =', content)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Updated index.html with new questions, 27 types, and updated dimensions.")
