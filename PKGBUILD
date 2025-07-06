# Maintainer: Saeed Badrelden <you@example.com>

pkgname=hel-sec-audit
pkgver=0.1.0
pkgrel=1
pkgdesc="Comprehensive Security Audit and Hardening Tool for Linux and Windows."
arch=('any')
url="https://github.com/helwan-linux/helwan-security"
license=('MIT')
depends=('python' 'python-pyqt5' 'python-psutil' 'python-netifaces')
source=("${pkgname}-${pkgver}.tar.gz::https://codeload.github.com/helwan-linux/helwan-security/tar.gz/refs/heads/main")
md5sums=('SKIP')

build() {
  :
}

package() {
  # إنشاء مجلد البرنامج داخل /opt
  install -d "${pkgdir}/opt/${pkgname}"

  # نسخ الملفات من مجلد hel-sec-audit الفرعي فقط
  cp -r "${srcdir}/helwan-security-main/hel-sec-audit/"* "${pkgdir}/opt/${pkgname}/"

  # جعل السكريبت الرئيسي قابل للتنفيذ
  chmod +x "${pkgdir}/opt/${pkgname}/main.py"

  # إنشاء رابط رمزي في /usr/bin لتشغيل البرنامج من التيرمنال
  install -d "${pkgdir}/usr/bin"
  ln -s "/opt/${pkgname}/main.py" "${pkgdir}/usr/bin/hel-sec-audit"

  # إنشاء مجلد التطبيقات ونسخ ملف .desktop
  install -d "${pkgdir}/usr/share/applications"
  install -m644 "${srcdir}/helwan-security-main/hel-sec-audit/hel-sec-audit.desktop" "${pkgdir}/usr/share/applications/"

  # نسخ أيقونة إذا كانت موجودة
  if [[ -f "${srcdir}/helwan-security-main/hel-sec-audit/icon.png" ]]; then
    install -d "${pkgdir}/usr/share/pixmaps"
    install -m644 "${srcdir}/helwan-security-main/hel-sec-audit/icon.png" "${pkgdir}/usr/share/pixmaps/hel-sec-audit.png"
  fi
}

