# PKGBUILD
# Arch Linux package build file for Hel-Sec-Audit

pkgname=hel-sec-audit
pkgver=0.1.0 # Initial package version, can be updated later
pkgrel=1
pkgdesc="Comprehensive Security Audit and Hardening Tool for Linux and Windows."
arch=('any') # 'any' as it's a Python script and works on any architecture
url="https://github.com/helwan-linux/helwan-security" # GitHub repository URL
license=('MIT') # Assuming MIT license, please verify and adjust if different.

# Python dependencies required by the application, mapped to Arch Linux package names
depends=('python' 'python-pyqt5' 'python-psutil' 'python-netifaces')

# Source is a tarball of the 'main' branch from the GitHub repository
# The extracted folder name from this tarball will be 'helwan-security-main/'
source=("${pkgname}-${pkgver}.tar.gz::${url}/archive/refs/heads/main.tar.gz")

# MD5 checksums - These need to be updated after the source file is downloaded for the first time.
# Use 'makepkg -g' to generate them after placing this PKGBUILD file in a directory.
# 'SKIP' can be used during development but is not recommended for production.
md5sums=('SKIP')

build() {
  # This section is for complex build steps (e.g., compilation).
  # For pure Python projects, it can be left empty or indicated with a colon ":".
  :
}

package() {
  # This section is responsible for installing files to their correct locations in the system.

  # Create the main application directory in /opt, a common place for third-party software
  install -d "${pkgdir}/opt/hel-sec-audit"

  # Copy all files from the extracted source directory to the installation directory
  # The extracted source from the tarball will be 'helwan-security-main'
  cp -r "${srcdir}/helwan-security-main/"* "${pkgdir}/opt/hel-sec-audit/"

  # Create the desktop applications directory
  install -d "${pkgdir}/usr/share/applications/"

  # Copy the .desktop file to make the application appear in the desktop environment's menu
  # The .desktop file is located directly inside the 'helwan-security-main' extracted folder
  install -m644 "${srcdir}/helwan-security-main/hel-sec-audit.desktop" "${pkgdir}/usr/share/applications/"

  # Make the main Python script executable
  chmod +x "${pkgdir}/opt/hel-sec-audit/main.py"
  
  # Optional: Ensure all Python scripts are executable (good practice for helper scripts)
  # find "${pkgdir}/opt/hel-sec-audit/" -name "*.py" -exec chmod +x {} \;
}