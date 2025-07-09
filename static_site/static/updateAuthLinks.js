// 全站统一登录状态检测与登出
async function updateAuthLinks() {
  try {
    console.log('开始更新认证链接...');
    console.log('当前页面URL:', window.location.href);
    
    // 添加时间戳防止缓存
    const timestamp = new Date().getTime();
    const resp = await fetch(`http://localhost:5002/api/check-auth?t=${timestamp}`, {
      method: 'GET',
      credentials: 'include',
      headers: {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'Cache-Control': 'no-cache',
        'Pragma': 'no-cache'
      }
    });
    
    console.log('API响应状态:', resp.status);
    console.log('API响应头:', Object.fromEntries(resp.headers.entries()));
    
    if (!resp.ok) {
      throw new Error(`HTTP error! status: ${resp.status}`);
    }
    
    const data = await resp.json();
    console.log('API响应数据:', data);
    
    const authLinks = document.getElementById('auth-links');
    if(!authLinks) {
      console.error('找不到auth-links元素');
      return;
    }
    
    console.log('找到auth-links元素:', authLinks);
    
    if(data.authenticated) {
      console.log('用户已登录，显示登出链接');
      authLinks.innerHTML = '<a href="#" id="logout-link">登出</a>';
      const logoutLink = document.getElementById('logout-link');
      if(logoutLink) {
        logoutLink.onclick = async function(e) {
          e.preventDefault();
          console.log('点击登出链接');
          await fetch('http://localhost:5002/api/logout', {method: 'POST', credentials: 'include'});
          location.reload();
        };
      }
    } else {
      console.log('用户未登录，显示登录/注册链接');
      authLinks.innerHTML = '<a href="/login.html" id="login-link">登录</a> <a href="/register.html" id="register-link">注册</a>';
    }
    
    console.log('认证链接更新完成');
  } catch (error) {
    console.error('更新认证链接失败:', error);
    console.error('错误详情:', error.message);
    // 如果API调用失败，默认显示登录/注册链接
    const authLinks = document.getElementById('auth-links');
    if(authLinks) {
      authLinks.innerHTML = '<a href="/login.html" id="login-link">登录</a> <a href="/register.html" id="register-link">注册</a>';
  }
  }
}
// 页面加载自动调用
if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', updateAuthLinks);
} else {
  updateAuthLinks();
}

// 确保在页面完全加载后再次检查
window.addEventListener('load', updateAuthLinks);

// 强制延迟执行，确保所有资源都加载完成
setTimeout(updateAuthLinks, 100);
setTimeout(updateAuthLinks, 500);
setTimeout(updateAuthLinks, 1000);

// 添加页面可见性变化监听，当页面重新可见时更新状态
document.addEventListener('visibilitychange', function() {
  if (!document.hidden) {
    updateAuthLinks();
  }
});

// 监听页面跳转事件
window.addEventListener('pageshow', function(event) {
  // 如果页面是从缓存恢复的，强制更新认证状态
  if (event.persisted) {
    updateAuthLinks();
  }
});

// 监听页面焦点事件
window.addEventListener('focus', function() {
  updateAuthLinks();
});

// 监听URL变化（用于单页应用）
let currentUrl = window.location.href;
setInterval(function() {
  if (window.location.href !== currentUrl) {
    currentUrl = window.location.href;
    updateAuthLinks();
  }
}, 100); 