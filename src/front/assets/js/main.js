/*
    Eventually by HTML5 UP
    html5up.net | @ajlkn
    Free for personal and commercial use under the CCA 3.0 license (html5up.net/license)
*/

(function() {

    "use strict";

    var $body = document.querySelector('body');

    // Methods/polyfills.

        // classList | (c) @remy | github.com/remy/polyfills | rem.mit-license.org
        !function(){function t(t){this.el=t;for(var n=t.className.replace(/^\s+|\s+$/g,"").split(/\s+/),i=0;i<n.length;i++)e.call(this,n[i])}function n(t,n,i){Object.defineProperty?Object.defineProperty(t,n,{get:i}):t.__defineGetter__(n,i)}if(!("undefined"==typeof window.Element||"classList"in document.documentElement)){var i=Array.prototype,e=i.push,s=i.splice,o=i.join;t.prototype={add:function(t){this.contains(t)||(e.call(this,t),this.el.className=this.toString())},contains:function(t){return-1!=this.el.className.indexOf(t)},item:function(t){return this[t]||null},remove:function(t){if(this.contains(t)){for(var n=0;n<this.length&&this[n]!=t;n++);s.call(this,n,1),this.el.className=this.toString()}},toString:function(){return o.call(this," ")},toggle:function(t){return this.contains(t)?this.remove(t):this.add(t),this.contains(t)}},window.DOMTokenList=t,n(Element.prototype,"classList",function(){return new t(this)})}}();

        // canUse
        window.canUse=function(p){if(!window._canUse)window._canUse=document.createElement("div");var e=window._canUse.style,up=p.charAt(0).toUpperCase()+p.slice(1);return p in e||"Moz"+up in e||"Webkit"+up in e||"O"+up in e||"ms"+up in e};

        // window.addEventListener
        (function(){if("addEventListener"in window)return;window.addEventListener=function(type,f){window.attachEvent("on"+type,f)}})();

    // Play initial animations on page load.
    window.addEventListener('load', function() {
        window.setTimeout(function() {
            $body.classList.remove('is-preload');
        }, 100);
    });

    // Slideshow Background.
    window.addEventListener('load', function() {
        // Settings.
        var settings = {
            images: {
                'images/bg01.jpg': 'center',
                'images/bg02.jpg': 'center',
                'images/bg03.jpg': 'center'
            },
            delay: 6000
        };

        // Vars.
        var pos = 0, lastPos = 0,
            $wrapper, $bgs = [], $bg, k;

        // Create BG wrapper and BGs.
        $wrapper = document.createElement('div');
        $wrapper.id = 'bg';
        $body.appendChild($wrapper);

        for (k in settings.images) {
            $bg = document.createElement('div');
            $bg.style.backgroundImage = 'url("' + k + '")';
            $bg.style.backgroundPosition = settings.images[k];
            $wrapper.appendChild($bg);
            $bgs.push($bg);
        }

        // Show the first image.
        $bgs[pos].classList.add('visible');
        $bgs[pos].classList.add('top');

        // Bail if we only have a single BG or the client doesn't support transitions.
        if ($bgs.length > 1 && canUse('transition')) {
            window.setInterval(function() {
                lastPos = pos;
                pos = (pos + 1) % $bgs.length;

                // Swap top images.
                $bgs[lastPos].classList.remove('top');
                $bgs[pos].classList.add('visible');
                $bgs[pos].classList.add('top');

                // Hide the last image after a short delay.
                window.setTimeout(function() {
                    $bgs[lastPos].classList.remove('visible');
                }, settings.delay / 2);
            }, settings.delay);
        }
    });

})();
