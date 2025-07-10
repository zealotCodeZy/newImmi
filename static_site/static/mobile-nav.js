// 响应式导航菜单控制
document.addEventListener('DOMContentLoaded', function() {
  const menuToggle = document.getElementById('menu-toggle');
  const navLinks = document.getElementById('nav-links');
  
  if (menuToggle && navLinks) {
    menuToggle.addEventListener('click', function() {
      navLinks.classList.toggle('show');
    });
    
    // 点击导航链接后自动收起菜单
    const navItems = navLinks.querySelectorAll('a');
    navItems.forEach(function(item) {
      item.addEventListener('click', function() {
        navLinks.classList.remove('show');
      });
    });
    
    // 点击页面其他地方时收起菜单
    document.addEventListener('click', function(event) {
      if (!menuToggle.contains(event.target) && !navLinks.contains(event.target)) {
        navLinks.classList.remove('show');
      }
    });
  }
}); 