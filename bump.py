# يحدّث رقم النسخة بالصفحتين، والصفحة تعيد تحميل نفسها إذا لقت نسخة أحدث
import re, sys, datetime
build = datetime.datetime.now(datetime.timezone.utc).strftime("%Y%m%d%H%M%S")
CHECK = '''<script>
(async () => {
  try {
    const cur = document.querySelector('meta[name="build"]').content;
    const r = await fetch(location.pathname + "?b=" + Date.now(), { cache: "no-store" });
    const m = (await r.text()).match(/<meta name="build" content="([^"]+)"/);
    if (m && m[1] !== cur && !sessionStorage.getItem("rl" + m[1])) {
      sessionStorage.setItem("rl" + m[1], "1");
      location.replace(location.pathname + "?v=" + m[1] + location.hash);
    }
  } catch (e) {}
})();
</script>
'''
for f in ["index.html", "admin.html"]:
    s = open(f, encoding="utf-8").read()
    if '<meta name="build"' in s:
        s = re.sub(r'<meta name="build" content="[^"]+">', f'<meta name="build" content="{build}">', s)
    else:
        s = s.replace('<meta charset="utf-8">', f'<meta charset="utf-8">\n<meta name="build" content="{build}">', 1)
        assert '<meta name="build"' in s, f
    if "rl\" + m[1]" not in s:
        i = s.rindex("</body>"); s = s[:i] + CHECK + s[i:]
    open(f, "w", encoding="utf-8").write(s)
print(build)
