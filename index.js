var nickname = '';
var headimg = '';
var platid = '2';
var area = '1';
var qq = '';
var wx = '';
var yyh = '';
var yycg = '';
var userinfo = {};
var getParam = function (name) {
  var search = document.location.search;
  var pattern = new RegExp("[?&]" + name + "\=([^&]+)", "g");
  var matcher = pattern.exec(search);
  var items = null;
  if (null != matcher) {
    try {
      items = decodeURIComponent(decodeURIComponent(matcher[1]));
    } catch (e) {
      try {
        items = decodeURIComponent(matcher[1]);
      } catch (e) {
        items = matcher[1];
      }
    }
  }
  return items;
};
var adtagID = getParam('ADTAG');
var ADTAG = typeof adtagID != 'undefined' && adtagID != "" && adtagID != null && adtagID != "null" ? adtagID.replace(
  /\./g, '_') : '';
EAS.SendClick({ e_c: 'dfm.a20240906main.main_' + ADTAG })

var ecodee = getParam('ecode');
var ecode = typeof ecodee != 'undefined' && ecodee != "" && ecodee != null && ecodee != "null" ? ecodee.replace(
  /\./g, '_') : '';

var u = navigator.userAgent;
if (u.indexOf('Android') > -1 || u.indexOf('Linux') > -1) { //安卓手机
  platid = 1;
} else if (u.indexOf('iPhone') > -1) { //苹果手机
  platid = 0;
} else if (u.indexOf('Windows Phone') > -1) { //winphone手机
  platid = 1;
}
if (/Android|webOS|iPhone|iPad|iPod|BlackBerry/i.test(navigator.userAgent)) {

} else {
  platid = 2;
}

function isQQ() {
  var sUserAgent = navigator.userAgent;
  var REGEXP_IOS_QQ = new RegExp("(iPad|iPhone|iPod).*? (IPad)?QQ\\/([\\d\\.]+)");
  var REGEXP_ANDROID_QQ = new RegExp("\\bV1_AND_SQI?_([\\d\\.]+)(.*? QQ\\/([\\d\\.]+))?", "ig");
  //is IOSQQ or AndroidQQ opening
  var isIphoneOs_QQ = REGEXP_IOS_QQ.test(sUserAgent);
  var isAndroid_QQ = REGEXP_ANDROID_QQ.test(sUserAgent);
  if (isIphoneOs_QQ || isAndroid_QQ) {
    return true;
  } else {
    return false;
  }
}

function isWeiXin() {
  return /MicroMessenger/gi.test(navigator.userAgent);
}

function is_pc() {
  var os = new Array("Android", "iPhone", "Windows Phone", "iPod", "BlackBerry", "MeeGo", "SymbianOS"); // 其他类型的移动操作系统类型，自行添加
  var info = navigator.userAgent;
  var len = os.length;
  for (var i = 0; i < len; i++) {
    if (info.indexOf(os[i]) > 0) {
      return false;
    }
  }
  return true;
}

var usertype = 0;// 0 未登录，1 未预约，2 已预约未绑定手机，3 已绑定手机
var iPosterCardId = 0;
var iPosterCardId_tmp = 1;
var limitOnce = 0;

var dfmUrl = 'https://df.qq.com/cp/a20240906main/index.html';
var shareUrl = 'https://df.qq.com/cp/a20240906main/index.html';
var sYuyueCount = '0';

//登录
function doLoginGame() {
  if (Milo.isWxApp()) {
    doWxLogin();
  } else if (Milo.isQQApp()) {
    doQqLogin();
  } else if (is_pc()) {
    Milo.loginByQQConnectAndWX();
  } else {
    openDialog('pop12');
  }
}

$(".login-qq").on("click", function () {
  doQqLogin();
})

// 跳转微信小程序
function openWXMini() {
  location.href = 'weixin://dl/business/?appid=wx1c36464bbea2507a&path=pages/index/index&query=&env_version=release';
}

$(".login-wx").on("click", function () {
  // doWxLogin();
  if (isSub == 1) {
    isSub = 0;
    openWXMini();
  } else {
    // $(".pop5-input").val(document.location.href);
    // makeCode("pop6-copy-box", document.location.href)
    // buildCode('p5-code', document.location.href);

    openDialog('pop5');
  }
})

function doWxLogin() {
  Milo.mobileLoginByWX({
    appId: 'wx1cd4fbe9335888fe', //游戏在微信的appid，默认为腾讯游戏活动号
    gameDomain: 'iu.qq.com',
    redirectUri: '', //授权页面，默认为系统默认的comm-htdocs/login/milosdkwx_mobile_redirect.html
    sUrl: '', //授权成功返回的页面，默认为当前页面
    scope: 'snsapi_userinfo', //默认静默授权
    lang: 'zh_CN', //返回的用户信息中省市的语言版本
    openlink: '', //openlink，如果设置了，则在处理微信登录的时候，会从第三方跳到微信中
  });
}
function doQqLogin() {
  Milo.mobileLoginByQQConnect({
    appId: '101491592',
    scope: 'get_user_info',
    state: 'STATE',
    redirectUri: "https://milo.qq.com/comm-htdocs/login/qc_redirect.html",
    sUrl: '', //登录之后的跳转地址
  });
}

//登出
function logout() {
  Milo.logout({
    // 退出回调
    callback: function () {
      location.reload();
      popMsg("注销成功");
    }
  });
}
if (Milo.get("acctype") == "wx" && Milo.get("appid") != "wx1cd4fbe9335888fe" && Milo.get("appid") != "wxfa0c35392d06b82f") {
  console.log("登录appid清理");
  Milo.logout({
    callback: function () {
      window.location.reload(true);
    }
  });
}
// 页面登录态度判断
$(function () {
  checklogin();
});
let EASopendid = '';
function checklogin() {
  console.log('进入 checklogin');
  Milo.checkLogin({
    iUseQQConnect: true, //如果当前活动使用的互联登录,请将改参数设置true
    success: function (user) {
      var userInfo = user && user.userInfo;
      EASopendid = userInfo.openid;
      console.log(userInfo);

      $("#logined").show();
      $("#unlogin").hide();
      $("#login_nickname_span").html(userInfo.nickName);
      if (Milo.isQQApp() || Milo.isWxApp()) {
        $(".out_btn").hide();
      }

      if (userInfo.acctype == 'qc') {
        area = 2;
      } else if (userInfo.acctype == 'wx') {
        area = 1;
      }

    },
    fail: function (res) {
      console.log('checklogin fail');
    }
  });
}


function doAMSAction(b) {
  Milo.checkLogin({
    iUseQQConnect: true, //如果当前活动使用的互联登录,请将改参数设置true
    success: function (user) {
      Milo.emit(b);
    },
    fail: function (res) {
      doLoginGame()
    }
  });
}

var isSub = 0;


var myreg = /^[1][3,4,5,6,7,8,9][0-9]{9}$/;

// 官网注册领取(验证)
function receiveGift() {
  hideVideo();
  Milo.checkLogin({
    iUseQQConnect: true, //如果当前活动使用的互联登录,请将改参数设置true
    success: function (user) {
      Milo.emit(flow_1072382);
    },
    fail: function (res) {
      doLoginGame()
    }
  });
}

var flow_1072382 = {
  actId: '670608',
  token: 'e992c1',
  sData: {},
  openToOpen: {
    sAMSTrusteeship: 1,
    ams_targetappid_qc: '1110543085',
    ams_targetappid_wx: 'wx39308a0a1bd83d22',
    oGopenidParams: {
      needGopenid: 1,
      isPreengage: 1
    }
  },
  success: function (res) {
    console.log(res);
    if (res.iRet == 0) {
      $('#pop_tips').text('奖励已发放到您的邮箱');
      openDialog('pop8')
    }
  },
  fail: function (res) {
    console.log(res);
    if (res.iRet == 101) {
      //todo 登录态失效，需要重新调登录方法 （开发自行实现）
    } else if (res.iRet == 99998) {
      // todo 调用提交绑定大区方法
    } else if (res.iRet == -9998) {
      // todo 关闭选择角色弹窗
    } else {
      popMsg(res.sMsg);
    }
  }
}

function popMsg(alertmsg) {
  commTip(alertmsg, time = 2000, "center");
}

var swiper = new Swiper('.p2_banner', {
  // pagination: {
  //   el: '.p2_pa',
  //   clickable :true,
  // },
  autoplay: {
    delay: 2000,
    stopOnLastSlide: false,
    disableOnInteraction: true,
  },
  observeParents: true,
  observer: true,
  on: {
    init(swiper) {
        var sw = this;
        $('.p2_text').on('click', 'a', function() {
            var i = $(this).index();
            $(this).addClass('on').siblings().removeClass('on');
            sw.slideTo(i);
        })
    },
    transitionStart: function (swiper) {
      // console.log('当前的slide序号是'+this.activeIndex);
      $('.p2_text a').eq(this.activeIndex).addClass('on').siblings().removeClass('on');
    },
  },
});



var p3Thumbs = new Swiper(".p3-thumbs", {
  // loop: true,
  direction: 'vertical',
  slidesPerView: 'auto',
  spaceBetween: 15,
  freeMode: true,
  watchSlidesProgress: true,
  observeParents: true,
  observer: true
});

var p3Top = new Swiper(".p3-top", {
  effect: 'fade',
  loop: true,
  allowTouchMove: false,
  navigation: {
    nextEl: ".p3-next",
    prevEl: ".p3-prev",
  },
  thumbs: {
    swiper: p3Thumbs,
  },
  on: {
    transitionStart: function (swiper) {
      // console.log('当前的slide序号是'+this.activeIndex);
      // if(this.activeIndex==1){
      //   p3Top.allowSlideNext= false;
      //   p3Thumbs.allowSlideNext= false;
      //   $('.p3-next').addClass('swiper-button-disabled');
      // }else{
      //   p3Top.allowSlideNext= true;
      //   p3Thumbs.allowSlideNext= true;
      //   $('.p3-next').removeClass('swiper-button-disabled');
      // }
    },
  },
  observeParents: true,
  observer: true,
});

var p3ThumbsSmall = new Swiper(".p3-thumbs-small", {
  effect: 'coverflow',
  loop: true,
  slidesPerView: 2.3,
  centeredSlides: true,
  coverflowEffect: {
    rotate: 0,
    stretch: '11.5%',
    depth: 60,
    modifier: 2,
    slideShadows: false
  },
  observeParents: true,
  observer: true,
  on: {
    transitionStart: function () {
      p3Top.slideTo(this.realIndex + 1);
    }
  }
})


var p4Thumbs = new Swiper(".p4-thumbs", {
  // loop: true,
  slidesPerView: 4.75,
  freeMode: true,
  watchSlidesProgress: true,
  observeParents: true,
  observer: true,
  nested: true,
  breakpoints: {
    751: {  //当屏幕宽度大于750
      direction: 'vertical',
      slidesPerView: 5.5
    }
  },
});
var p4Top = new Swiper('.p4-top', {
  effect: 'fade',
  allowTouchMove: false,
  spaceBetween: 10,
  // loop:true,
  navigation: {
    nextEl: '.p4-next',
    prevEl: '.p4-prev',
  },
  thumbs: {
    swiper: p4Thumbs,
  },
  observeParents: true,
  observer: true,
});


$(".p4-top").on("click", ".p4_con .p4_desc", function () {
  $(this).addClass("act").siblings().removeClass("act");
})



var p5Thumbs = new Swiper('.p5-thumbs', {
  slidesPerView: 4.4,
  watchSlidesProgress: true,
  observeParents: true,
  observer: true,
  breakpoints: {
    750: {
      slidesPerView: 4.6,
    },
    1024: {
      slidesPerView: 7,
    }
  },
  // on: {
  //   click: function() {
  //     var thumbIndex = $(".p5-thumbs .swiper-slide-thumb-active").index();
  //   }
  // }
});

var p5Top = new Swiper('.p5-top', {
  effect: 'fade',
  allowTouchMove: true,
  loop: true,
  navigation: {
    nextEl: '.p5-next',
    prevEl: '.p5-prev',
  },
  thumbs: {
    swiper: p5Thumbs,
  },
  observeParents: true,
  observer: true,
  breakpoints: {
    750: {
      allowTouchMove: false,
    }
  }
});

// var p5NavSw = new Swiper('.p5-nav-swiper', {
//   effect: 'coverflow',
//   slidesPerView: 3.6,
//   slideToClickedSlide: true,
//   loop: true,
//   centeredSlides: true,
//   coverflowEffect: {
//     rotate: 0,
//     stretch: 0,
//     depth: 100,
//     modifier: 2,
//     slideShadows: false
//   },
//   on: {
//     // transitionEnd: function() {
//     //   $(".p5-nav li").eq(this.realIndex).addClass("act").siblings().removeClass("act");
//     //   $(".p5-top .swiper-slide, .p5-thumbs .swiper-slide").addClass('hide');
//     //   switch(true) {
//     //     case this.realIndex === 0 : $(".part5 .swiper-slide.p5-bq").removeClass('hide'); break;
//     //     case this.realIndex === 1 : $(".part5 .swiper-slide.p5-cfq").removeClass('hide'); break;
//     //     case this.realIndex === 2 : $(".part5 .swiper-slide.p5-qjq").removeClass('hide'); break;
//     //     case this.realIndex === 3 : $(".part5 .swiper-slide.p5-xdq").removeClass('hide'); break;
//     //   }
//     //   p5Top.update();
//     //   p5Thumbs.update();
//     //   p5Top.slideTo(0);
//     //   p5Thumbs.slideTo(0);
//     // }
//   }
// })

// $(".p5-nav li").bind("click", function() {
//   $(this).addClass("act").siblings().removeClass("act");
//   p5NavSw.slideTo($(this).index());
// })

var p6Thumbs = new Swiper('.p6-thumbs', {
  slidesPerView: 4.55,
  freeMode: true,
  watchSlidesProgress: true,
  observeParents: true,
  observer: true,
  nested: true,
  breakpoints: {
    751: {  //当屏幕宽度大于750
      direction: 'vertical',
      slidesPerView: 5.5
    }
  },
});

var p6Top = new Swiper('.p6-top', {
  effect: 'fade',
  allowTouchMove: false,
  loop: true,
  navigation: {
    nextEl: '.p6-next',
    prevEl: '.p6-prev',
  },
  thumbs: {
    swiper: p6Thumbs,
  },
  observeParents: true,
  observer: true,
});


// 视频
// window.mySvid = "k1194rb22mx";
var player = null;
function playVideo(mySvid) {
  openDialog("vindex-play");
  if (player) { player.destroy(); }
  player = new window.SuperPlayer({
    // 传入需要展示播放器的容器选择器
    container: '.video-container',
  });
  player.play({
    vid: mySvid,
  });
}
function hideVideo() {
  closeDialog();
  if (player) { player.destroy(); }
  $(".video-container").html("");
}


//------------资讯----------------
function getDate(type, dateTimeStr) {
  var dateOnly = dateTimeStr.split(' ')[0];
  // 提取月和日部分
  var year = dateOnly.split('-')[0]; // 提取年份
  var month = dateOnly.split('-')[1]; // 提取月份
  var day = dateOnly.split('-')[2];   // 提取日期
  // 格式化为 MM-DD
  if (type < 1) {
    return month + '-' + day;
  } else {
    return year + '-' + month + '-' + day;
  }
}

var mLimit = 1;//每页获取的数量
var maxPageNum = 1;//最大页数
var thisPage = 1;//当前页

function getNews(isTop, chanid, typeids, limit = 6, start = 0) {
  console.log("isTop", isTop);
  var flow_1073310 = {
    actId: '670608',
    token: 'd46289',
    sData: {
      chanid: chanid, // 渠道id
      typeids: typeids, // 召回内容类型，1：资讯，2：视频，可以同时传入，英文逗号分隔；默认拉取资讯
      limit: limit, // 单次查询数量
      start: start, // 偏移量
    },
    success: function (res) {
      console.log(res);
      if (res.iRet == 0) {
        if (res.details.jData.data.total >= 0) {

          mLimit = limit;
          maxPageNum = Math.ceil(Number(res.details.jData.data.total) / mLimit);
          thisPage = Math.floor(start / mLimit) + 1;

          var newsData = res.details.jData.data.items;
          switch (isTop) {
            case 0://最重要
              const $newsLink = $('.p2_newt a');
              const $newsTitle1 = $('.newsTitle1');
              $newsTitle1.text(newsData[0].sTitle);
              // 设置链接的 href 属性，带上 id 参数
              const url = `https://df.qq.com/cp/a20240906main/newsdetail.html?id=${newsData[0].iDocID}`;
              $newsLink.attr('href', url);
              $newsLink.attr('target', '_blank'); // 在新窗口或新标签页中打开链接
              return false;
            case 1://首页资讯列表
              const $topNewsList = $('#newsList');
              if ($topNewsList.find('li').length > 0) {
                $topNewsList.empty();
              }
              newsData.forEach(news => {
                const $li = $('<li></li>');
                const $a = $('<a></a>');
                const tipsTop = tips(news.sChannel);
                const $i = $('<i class="newsType"></i>').text(tipsTop[1]);
                if (tipsTop[0]) { $i.addClass(tipsTop[0]); }
                const $p = $('<p class="newsTitle"></p>').text(news.sTitle);
                const $span = $('<span class="newsTime"></span>').text(getDate(0, news.sIdxTime));
                // 设置链接的 href 属性，带上 id 参数
                const url = `https://df.qq.com/cp/a20240906main/newsdetail.html?id=${news.iDocID}`;
                $a.attr('href', url);
                $a.attr('target', '_blank'); // 在新窗口或新标签页中打开链接
                $a.append($i, $p, $span);
                $li.append($a);
                $topNewsList.append($li);
              });
              return false;
            case 2:// 首页视频列表
              const $topVidList = $('#vidList');
              if ($topVidList.find('li').length > 0) {
                $topVidList.empty();
              }
              newsData.forEach(news => {
                const $li = $('<li></li>');
                const $a = $('<a></a>');
                const $img = $('<img>').attr('src', news.sIMG).attr('alt', '');
                const $i = $('<i></i>');
                const $p = $('<p></p>').text(news.sTitle);
                const $div = $('<div class="p2_desc"></div>');
                const $viewsSpan = $('<span></span>').text(news.iTotalPlay);
                const $dateSpan = $('<span></span>').text(getDate(1, news.sIdxTime));
                const creatTime = getDate(1, news.sIdxTime);
                // 设置链接的点击事件，执行 playVideo 方法
                $a.on('click', function (event) {
                  //event.preventDefault(); // 阻止默认的链接跳转行为
                  const url = `https://df.qq.com/cp/a20240906main/videodetail.html?id=${news.sVID}&chanid=${chanid}&totalPlay=${news.iTotalPlay}&creatTime=${creatTime}&title=${news.sTitle}&idocId=${news.iDocID}&from=1`;
                  $a.attr('href', url);
                  //playVideo(news.sVID); // 执行 playVideo 方法
                  //playUp(news.iDocID);
                });
                $div.append($viewsSpan, $dateSpan);
                $a.append($img, $i, $p, $div);
                $li.append($a);
                $topVidList.append($li);
              });
              return false;
            case 3:
              const $newsList = $('.newsbox ul');
              if ($newsList.find('li').length > 0) {
                $newsList.empty();
              }
              renderPagination(maxPageNum, thisPage, chanid, 3);
              $('#jumpId').val(thisPage);
              $('.page_num').on('click', function () {
                videoJumpPage(null, chanid, 3)
              })
              // 遍历新闻数据并生成列表项
              newsData.forEach(news => {
                const $li = $('<li></li>');
                const $a = $('<a></a>');
                const $img = $('<img>').attr('src', news.sCoverList[1]['url']).attr('alt', '');
                const tipsTop = tips(news.sChannel);
                const $i = $('<i class="newsType"></i>').text(tipsTop[1]);
                if (tipsTop[0]) { $i.addClass(tipsTop[0]); }
                const $h2 = $('<h2></h2>').text(news.sTitle);
                const $p = $('<p></p>').text(news.sDesc);
                const $span = $('<span></span>').text(getDate(0, news.sIdxTime));
                // 设置链接的 href 属性，带上 id 参数
                const url = `https://df.qq.com/cp/a20240906main/newsdetail.html?id=${news.iDocID}`;
                $a.attr('href', url);
                $a.attr('target', '_blank'); // 在新窗口或新标签页中打开链接
                // 组装元素
                $a.append($img, $i, $h2, $p, $span);
                $li.append($a);
                $newsList.append($li);
              });



              return false;
            case 4:
              const $vidList = $('.p2_vidbox ul');
              if ($vidList.find('li').length > 0) {
                $vidList.empty();
              }
              // 遍历新闻数据并生成列表项
              renderPagination(maxPageNum, thisPage, chanid, 4);
              $('#jumpId').val(thisPage);
              $('.page_num').on('click', function () {
                videoJumpPage(null, chanid, 4)
              })
              newsData.forEach(news => {
                const $li = $('<li></li>');
                const $a = $('<a></a>');
                const $img = $('<img>').attr('src', news.sIMG).attr('alt', '');
                const $i = $('<i></i>').text(news.sTagIds);
                const $p = $('<p></p>').text(news.sTitle);
                const $div = $('<div></div>').addClass('p2_desc');
                const $viewsSpan = $('<span></span>').text(news.iTotalPlay);
                const $dateSpan = $('<span></span>').text(getDate(1, news.sIdxTime));
                //修改跳转
                const creatTime = getDate(1, news.sIdxTime);
                // 设置链接的点击事件，执行 playVideo 方法
                $a.on('click', function (event) {
                  const url = `https://df.qq.com/cp/a20240906main/videodetail.html?id=${news.sVID}&chanid=${chanid}&totalPlay=${news.iTotalPlay}&creatTime=${creatTime}&title=${news.sTitle}&idocId=${news.iDocID}&from=2`;
                  $a.attr('href', url);
                  // event.preventDefault(); // 阻止默认的链接跳转行为
                  // playVideo(news.sVID); // 执行 playVideo 方法
                  // playUp(news.iDocID);
                });

                // 组装元素
                $div.append($viewsSpan, $dateSpan);
                $a.append($img, $i, $p, $div);
                $li.append($a);
                $vidList.append($li);
              });
          }
        }
      }
    },
    fail: function (res) {
      if (res.iRet == 101) {
        //todo 登录态失效，需要重新调登录方法 （开发自行实现）
      } else if (res.iRet == 99998) {
        // todo 调用提交绑定大区方法
      }
      console.log(res);
    }
  }
  Milo.emit(flow_1073310);
}
var NewsArr = {
  1: '6895',
  2: '6896',
  3: '6898',
  4: '7037' // 新增赛事模块20250805,author:supersu
}
var VidArr = {
  1: '6910',//首页-官方视频
  2: '6911',//首页-攻略教学
  3: '6912',//首页-开发日志
  4: '6913',//首页-精品栏目
}
var VidListArr = {
  1: '6904',//官方视频
  2: '6907',//攻略教学
  3: '6908',//开发日志
  4: '6909',//精品栏目
}
$(document).ready(function () {
  const p2_tab1 = $('.p2_tab1');
  p2_tab1.click(function () {
    // 移除所有 a 标签的 'on' 类
    p2_tab1.removeClass('on');
    // 为被点击的 a 标签添加 'on' 类
    $(this).addClass('on');
    // 获取被点击的 a 标签的索引
    var index = p2_tab1.index(this);
    // 输出索引
    console.log("点击了第 " + (index + 1) + " 个标签");
    getNews(1, NewsArr[(index + 1)], 1, 6);
  });

  const p2_tab2 = $('.p2_tab2');
  p2_tab2.click(function () {
    // 移除所有 a 标签的 'on' 类
    p2_tab2.removeClass('on');
    // 为被点击的 a 标签添加 'on' 类
    $(this).addClass('on');
    // 获取被点击的 a 标签的索引
    var index = p2_tab2.index(this);
    // 输出索引
    console.log("点击了第 " + (index + 1) + " 个标签");
    getNews(2, VidArr[(index + 1)], 2, 4)
  });

  var tab = 1;

  const p2_tab3 = $('.p2_tab3');
  p2_tab3.click(function () {
    // 移除所有 a 标签的 'on' 类
    p2_tab3.removeClass('on');
    // 为被点击的 a 标签添加 'on' 类
    $(this).addClass('on');
    // 获取被点击的 a 标签的索引
    var index = p2_tab3.index(this);
    tab = (index + 1);
    // 输出索引
    console.log("点击了第 " + (index + 1) + " 个标签");
    getNews(3, NewsArr[(index + 1)], 1, 9);
  });

  const p2_tab4 = $('.p2_tab4');
  p2_tab4.click(function () {
    // 移除所有 a 标签的 'on' 类
    p2_tab4.removeClass('on');
    // 为被点击的 a 标签添加 'on' 类
    $(this).addClass('on');
    // 获取被点击的 a 标签的索引
    var index = p2_tab4.index(this);
    tab = (index + 1);
    // 输出索引
    console.log("点击了第 " + (index + 1) + " 个标签");
    getNews(4, VidListArr[(index + 1)], 2, 8);
  });


  $('.news_page1 a').eq(0).click(function () {
    var nextPage = thisPage <= 1 ? 1 : (thisPage - 1);
    if (nextPage == thisPage || nextPage < 1) {
      return false;
    } else {
      console.log(typeId)
      var start = (nextPage - 1) * mLimit;
      getNews(3, NewsArr[tab], typeId, mLimit, start)
    }
  })

  $('.news_page1 a').eq(1).click(function () {
    var nextPage = thisPage >= maxPageNum ? thisPage : (thisPage + 1);
    if (nextPage == thisPage || nextPage == 1) {
      return false;
    } else {
      console.log(typeId)
      var start = (nextPage - 1) * mLimit;
      getNews(3, NewsArr[tab], typeId, mLimit, start)
    }
  })



  $('.news_page2 a').eq(0).click(function () {
    var nextPage = thisPage <= 1 ? 1 : (thisPage - 1);
    if (nextPage == thisPage || nextPage < 1) {
      return false;
    } else {
      console.log(typeId)
      var start = (nextPage - 1) * mLimit;
      getNews(4, VidListArr[tab], typeId, mLimit, start)
    }
  })

  $('.news_page2 a').eq(1).click(function () {
    var nextPage = thisPage >= maxPageNum ? thisPage : (thisPage + 1);
    if (nextPage == thisPage || nextPage == 1) {
      return false;
    } else {
      console.log(typeId)
      var start = (nextPage - 1) * mLimit;
      console.log("tab111", tab);
      getNews(4, VidListArr[tab], typeId, mLimit, start)
    }
  })



});

// 判断是否为数字（包括字符串类型的数字）
function isNumeric(value) {
  // 如果是数字类型，直接返回true
  if (typeof value === 'number') {
    return !isNaN(value) && isFinite(value);
  }

  // 如果是字符串，尝试转换为数字
  if (typeof value === 'string') {
    // 去除前后空格
    value = value.trim();

    // 空字符串不是数字
    if (value === '') {
      return false;
    }

    // 尝试转换为数字
    const num = Number(value);

    // 检查是否为有效数字且不是NaN
    return !isNaN(num) && isFinite(num);
  }

  // 其他类型都不是数字
  return false;
}

// 将值转换为数字（如果可能）
function toNumber(value, defaultValue = 0) {
  if (isNumeric(value)) {
    return Number(value);
  }
  return defaultValue;
}

function videoJumpPage(page, tab, type) {

  if (page === null) {
    page = $('#jumpId').val();
    // 使用新的数字验证函数
    if (!isNumeric(page)) {
      page = 1;
    } else {
      page = toNumber(page);
    }
  }

  console.log(page);

  console.log(page);
  let nextPage = page > maxPageNum ? maxPageNum : page;

  console.log(typeId)
  var start = (nextPage - 1) * mLimit;
  console.log("start", start)
  getNews(type, tab, typeId, mLimit, start)
}

function tips(values) {
  let result = ['', '']; // 默认返回值
  $.each(values, function (index, value) {
    if (value === 6896) {
      console.log(1);
      result = ['', '公告'];
      return false; // 中断循环
    } else if (value === 6898) {
      console.log(2);
      result = ['xw', '新闻'];
      return false; // 中断循环
    } else if (value === 7037) {
      console.log(3);
      result = ['', '赛事'];
      return false; // 中断循环
    }
  });
  return result;
}

function playUp(id) {
  var flow_1076230 = {
    actId: '670608',
    token: '257dde',
    sData: {
      id: id,
    },
    success: function (res) {
      console.log(res);
    },
    fail: function (res) {
      if (res.iRet == 101) {
        //todo 登录态失效，需要重新调登录方法 （开发自行实现）
      } else if (res.iRet == 99998) {
        // todo 调用提交绑定大区方法
      }
      console.log(res);
    }
  }
  Milo.emit(flow_1076230);
}

// 渲染分页
function renderPagination(totalPages, currentPage, chanid, type) {
  console.log(totalPages, currentPage, chanid, type);

  let $html = "";

  // 如果总页数小于等于7，显示所有页码
  if (totalPages <= 7) {
    for (let i = 1; i <= totalPages; i++) {
      if (i == currentPage) {
        $html += `<span class="on">${i}</span>`;
      } else {
        $html += `<span onclick="videoJumpPage(${i}, ${chanid}, ${type})">${i}</span>`;
      }
    }
  } else {
    // 总页数大于7，采用智能分页逻辑

    // 总是显示第一页
    if (currentPage == 1) {
      $html += `<span class="on">1</span>`;
    } else {
      $html += `<span onclick="videoJumpPage(1, ${chanid}, ${type})">1</span>`;
    }

    // 计算需要显示的页码范围
    let startPage = Math.max(2, currentPage - 2);
    let endPage = Math.min(totalPages - 1, currentPage + 2);

    // 如果当前页在前5页，显示前5页
    if (currentPage < 5) {
      startPage = 2;
      endPage = Math.min(5, totalPages - 1);
    }
    // 如果当前页在后2页，显示后2页
    else if (currentPage >= totalPages - 1) {
      startPage = Math.max(2, totalPages - 4);
      endPage = totalPages - 1;
    }

    // 添加第一个省略号（如果当前页不在前5页）
    if (currentPage >= 5) {
      $html += `<span>...</span>`;
    }

    // 显示中间页码
    for (let i = startPage; i <= endPage; i++) {
      if (i == currentPage) {
        $html += `<span class="on">${i}</span>`;
      } else {
        $html += `<span onclick="videoJumpPage(${i}, ${chanid}, ${type})">${i}</span>`;
      }
    }

    // 添加第二个省略号（如果当前页不在后2页）
    if (currentPage < totalPages - 1) {
      $html += `<span>...</span>`;
    }

    // 总是显示最后一页
    if (currentPage == totalPages) {
      $html += `<span class="on">${totalPages}</span>`;
    } else {
      $html += `<span onclick="videoJumpPage(${totalPages}, ${chanid}, ${type})">${totalPages}</span>`;
    }
  }

  $('.page_a').html($html);
}


$(".p7_nav a").bind("click", function () {
  $(this).addClass('on').siblings().removeClass('on');
  var i = $(this).index() == 2 ? '1' : $(this).index();
  $('.p7_con').eq(i).show().siblings().hide();
});

$(".p7-more.more1").bind("click", function () {
  $('.p7_con').eq(1).show().siblings().hide();
})

$(".p7-more.more2").bind("click", function () {
  $('.p7_con').eq(0).show().siblings().hide();
})



var p7Thumbs1 = null;
var p7Thumbs2 = null;


function resizeP7Swiper() {
  if (window.innerWidth <= 750) {
    if (!p7Thumbs1) { return; }
    p7Thumbs1.destroy(true, true);
    p7Thumbs2.destroy(true, true);
    p7Thumbs1 = null;
    p7Thumbs2 = null;
    $('.p7_tab1 p.act').removeClass('act');
    $('.p7_tab2 p.act').removeClass('act');
    $('.p7_tab1 .swiper-slide').eq(0).find('p').addClass('act');
    $('.p7_tab2 .swiper-slide').eq(0).find('p').addClass('act');
    $('.p7_box1 .p7_desc').eq(0).addClass('on').siblings().removeClass('on');
    $('.p7_box2 .p7_desc').eq(0).addClass('on').siblings().removeClass('on');
  } else {
    if (p7Thumbs1) { return; }
    p7Thumbs1 = new Swiper(".p7_tab1", {
      loop: true,
      slideToClickedSlide: true,
      direction: 'vertical',
      slidesPerView: 'auto',
      centeredSlides: true,
      loopedSlides: 7,
      observeParents: true,
      observer: true,
      on: {
        transitionStart: function (swiper) {
          $('.p7_box1 .p7_desc').eq(this.realIndex).addClass('on').siblings().removeClass('on');
        },
      },
    });
    p7Thumbs2 = new Swiper(".p7_tab2", {
      loop: true,
      slideToClickedSlide: true,
      direction: 'vertical',
      slidesPerView: 'auto',
      centeredSlides: true,
      loopedSlides: 7,
      observeParents: true,
      observer: true,
      on: {
        transitionStart: function (swiper) {
          $('.p7_box2 .p7_desc').eq(this.realIndex).addClass('on').siblings().removeClass('on');
        },
      },
    });
  }
};
resizeP7Swiper();
$(window).bind('resize', function () {
  resizeP7Swiper();
});

$('.p7_tab1').on('click', '.swiper-slide', function () {
  if (window.innerWidth > 750) { return; }
  $('.p7_tab1 p.act').removeClass('act');
  $(this).find('p').addClass('act');
  $('.p7_box1 .p7_desc').eq($(this).index()).addClass('on').siblings().removeClass('on');
})
$('.p7_tab2').on('click', '.swiper-slide', function () {
  if (window.innerWidth > 750) { return; }
  $('.p7_tab2 p.act').removeClass('act');
  $(this).find('p').addClass('act');
  $('.p7_box2 .p7_desc').eq($(this).index()).addClass('on').siblings().removeClass('on');
})