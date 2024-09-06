{pkgs}: {
  deps = [
    pkgs.python312Packages.virtualenv
    pkgs.python312Packages.gunicorn
    pkgs.libev
  ];
}
