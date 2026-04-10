sidebar_html = '''<nav id="sidebar">\
            <ul>\
                <a href="/"><li id="kp1" class="keypress"><span>Home</span><span class="keycap">1</span></li></a>\
                <a href="/#projects"><li id="kp2" class="keypress"><span>Projects</span><span class="keycap">2</span></li></a>\
                <a href="/#about"><li id="kp3" class="keypress"><span>About</span><span class="keycap">3</span></li></a>\

                <li class="listsep"></li>\
                <a href="/blog/"><li id="kpB" class="keypress"><span>Blog</span><span class="keycap">B</span></li></a>\
\
            </ul>\
        </nav>'''


sidebar_blog_html = '''
                <a href="/"><li id="kpH" class="keypress"><span>Home</span><span class="keycap">H</span></li></a>\
            </ul>\
        </nav>'''

sonne_var("sidebar", sidebar_html)
sonne_var("sidebar_blog", sidebar_blog_html)
