(function(a, b, c) {
	function d(a) {
		a = a || location.href;
		return "#" + a.replace(/^[^#]*#?(.*)$/, "$1")
	}
	var f = "hashchange",
	h = document,
	n, g = a.event.special,
	p = h.documentMode,
	j = "on" + f in b && (p === c || p > 7);
	a.fn[f] = function(a) {
		return a ? this.bind(f, a) : this.trigger(f)
	};
	a.fn[f].delay = 50;
	g[f] = a.extend(g[f], {
		setup: function() {
			if (j) return false;
			a(n.start)
		},
		teardown: function() {
			if (j) return false;
			a(n.stop)
		}
	});
	n = function() {
		function g() {
			var c = d(),
			j = F(q);
			if (c !== q) aa(q = c, j),
			a(b).trigger(f);
			else if (j !== q) location.href = location.href.replace(/#.*/, "") + j;
			p = setTimeout(g, a.fn[f].delay)
		}
		var n = {},
		p, q = d(),
		w = function(a) {
			return a
		},
		aa = w,
		F = w;
		n.start = function() {
			p || g()
		};
		n.stop = function() {
			p && clearTimeout(p);
			p = c
		};
		a.browser.msie && ! j && function() {
			var b, c;
			n.start = function() {
				if (!b) c = (c = a.fn[f].src) && c + d(),
				b = a('<iframe tabindex="-1" title="empty"/>').hide().one("load", function() {
					c || aa(d());
					g()
				}).attr("src", c || "javascript:0").insertAfter("body")[0].contentWindow,
				h.onpropertychange = function() {
					try {
						if (event.propertyName === "title") b.document.title = h.title
					} catch(a) {}
				}
			};
			n.stop = w;
			F = function() {
				return d(b.location.href)
			};
			aa = function(c, g) {
				var d = b.document,
				j = a.fn[f].domain;
				if (c !== g) d.title = h.title,
				d.open(),
				j && d.write('<script>document.domain="' + j + '"<\/script>'),
				d.close(),
				b.location.hash = c
			}
		} ();
		return n
	} ()
})(jQuery, this);
(function() {
	function a(i, a) {
		i || (i = {});
		for (var e in a) i[e] = a[e];
		return i
	}
	function b(i, a) {
		return parseInt(i, a || 10)
	}
	function c(i) {
		return typeof i == "string"
	}
	function d(i) {
		return typeof i == "object"
	}
	function f(i) {
		return typeof i == "number"
	}
	function h(i, a) {
		for (var e = i.length; e--;) if (i[e] == a) {
			i.splice(e, 1);
			break
		}
	}
	function n(i) {
		return i !== ya && i !== null
	}
	function g(i, a, e) {
		var b, g;
		if (c(a)) n(e) ? i.setAttribute(a, e) : i && i.getAttribute && (g = i.getAttribute(a));
		else if (n(a) && d(a)) for (b in a) i.setAttribute(b, a[b]);
		return g
	}
	function p(a) {
		if (!a || a.constructor != Array) a = [a];
		return a
	}
	function j() {
		var a = arguments,
		l, e, b = a.length;
		for (l = 0; l < b; l++) if (e = a[l], typeof e !== "undefined" && e !== null) return e
	}
	function o(a) {
		var l = "",
		e;
		for (e in a) l += ub(e) + ":" + a[e] + ";";
		return l
	}
	function m(i, l) {
		if (D && l && l.opacity !== ya) l.filter = "alpha(opacity=" + l.opacity * 100 + ")";
		a(i.style, l)
	}
	function t(i, l, e, b, c) {
		i = A.createElement(i);
		l && a(i, l);
		c && m(i, {
			padding: 0,
			border: Na,
			margin: 0
		});
		e && m(i, e);
		b && b.appendChild(i);
		return i
	}
	function q(a, l) {
		vb = j(a, l.animation)
	}
	function w() {
		var a = za.global.useUTC;
		wb = a ? Date.UTC: function(a, i, b, c, g, d) {
			return (new Date(a, i, j(b, 1), j(c, 0), j(g, 0), j(d, 0))).getTime()
		};
		Ib = a ? "getUTCMinutes": "getMinutes";
		Jb = a ? "getUTCHours": "getHours";
		Kb = a ? "getUTCDay": "getDay";
		pb = a ? "getUTCDate": "getDate";
		xb = a ? "getUTCMonth": "getMonth";
		yb = a ? "getUTCFullYear": "getFullYear";
		ec = a ? "setUTCMinutes": "setMinutes";
		fc = a ? "setUTCHours": "setHours";
		Lb = a ? "setUTCDate": "setDate";
		gc = a ? "setUTCMonth": "setMonth";
		hc = a ? "setUTCFullYear": "setFullYear"
	}
	function aa(a) {
		Ka || (Ka = t($a));
		a && Ka.appendChild(a);
		Ka.innerHTML = ""
	}
	function F(i, l) {
		var e = function() {};
		e.prototype = new i;
		a(e.prototype, l);
		return e
	}
	function Ma(a, l, e, c) {
		var g = za.lang,
		d = isNaN(l = Y(l)) ? 2: l,
		l = e === void 0 ? g.decimalPoint: e,
		c = c === void 0 ? g.thousandsSep: c,
		g = a < 0 ? "-": "",
		e = b(a = Y( + a || 0).toFixed(d)) + "",
		j = (j = e.length) > 3 ? j % 3: 0;
		return g + (j ? e.substr(0, j) + c: "") + e.substr(j).replace(/(\d{3})(?=\d)/g, "$1" + c) + (d ? l + Y(a - e).toFixed(d).slice(2) : "")
	}
	function M() {}
	function Q(i, l) {
		function e(i, e) {
			function l(a, i) {
				this.pos = a;
				this.minor = i;
				this.isNew = true;
				i || this.addLabel()
			}
			function c(a) {
				if (a) this.options = a,
				this.id = a.id;
				return this
			}
			function s() {
				var a = [],
				i = [],
				l;
				v = Ga = null;
				F = [];
				y(la, function(b) {
					l = false;
					y(["xAxis", "yAxis"], function(a) {
						if (b.isCartesian && (a == "xAxis" && H || a == "yAxis" && ! H) && (b.options[a] == e.index || b.options[a] === ya && e.index === 0)) b[a] = fa,
						F.push(b),
						l = true
					}); ! b.visible && B.ignoreHiddenSeries && (l = false);
					if (l) {
						var c, s, g, d, f;
						if (!H) {
							c = b.options.stacking;
							Ia = c == "percent";
							if (c) d = b.type + j(b.options.stack, ""),
							f = "-" + d,
							b.stackKey = d,
							s = a[d] || [],
							a[d] = s,
							g = i[f] || [],
							i[f] = g;
							Ia && (v = 0, Ga = 99)
						}
						b.isCartesian && (y(b.data, function(a) {
							var i = a.x,
							e = a.y,
							l = e < 0,
							b = l ? g: s,
							l = l ? f: d;
							v === null && (v = Ga = a[I]);
							H ? i > Ga ? Ga = i: i < v && (v = i) : n(e) && (c && (b[i] = n(b[i]) ? b[i] + e: e), e = b ? b[i] : e, a = j(a.low, e), Ia || (e > Ga ? Ga = e: a < v && (v = a)), c && (z[l] || (z[l] = {}), z[l][i] = {
								total: e,
								cum: e
							}))
						}), /(area|column|bar)/.test(b.type) && ! H && (v >= 0 ? (v = 0, eb = true) : Ga < 0 && (Ga = 0, ob = true)))
					}
				})
			}
			function g(a, i) {
				var l;
				U = i ? 1: N.pow(10, ha(N.log(a) / N.LN10));
				l = a / U;
				i || (i = [1, 2, 2.5, 5, 10], e.allowDecimals === false && (U == 1 ? i = [1, 2, 5, 10] : U <= 0.1 && (i = [1 / U])));
				for (var b = 0; b < i.length; b++) if (a = i[b], l <= (i[b] + (i[b + 1] || i[b])) / 2) break;
				a *= U;
				return a
			}
			function d(a) {
				var i;
				i = a;
				n(U) && (i = (U < 1 ? x(1 / U) : 1) * 10, i = x(a * i) / i);
				return i
			}
			function f() {
				var a, l, b, c, s = e.tickInterval,
				C = e.tickPixelInterval;
				a = e.maxZoom || (H ? Da(i.smallestInterval * 5, Ga - v) : null);
				D = m ? oa: ea;
				Qa ? (b = i[H ? "xAxis": "yAxis"][e.linkedTo], c = b.getExtremes(), V = j(c.min, c.dataMin), X = j(c.max, c.dataMax)) : (V = j(Ha, e.min, v), X = j(Ya, e.max, Ga));
				X - V < a && (c = (a - X + V) / 2, V = G(V - c, j(e.min, V - c), v), X = Da(V + a, j(e.max, V + a), Ga));
				if (!Fa && ! Ia && ! Qa && n(V) && n(X)) {
					a = X - V || 1;
					if (!n(e.min) && ! n(Ha) && L && (v < 0 || ! eb)) V -= a * L;
					if (!n(e.max) && ! n(Ya) && M && (Ga > 0 || ! ob)) X += a * M
				}
				K = V == X ? 1: Qa && ! s && C == b.options.tickPixelInterval ? b.tickInterval: j(s, Fa ? 1: (X - V) * C / D); ! R && ! n(e.tickInterval) && (K = g(K));
				fa.tickInterval = K;
				Ka = e.minorTickInterval === "auto" && K ? K / 5: e.minorTickInterval;
				if (R) {
					ba = [];
					var s = za.global.useUTC,
					E = 1E3 / Oa,
					J = 6E4 / Oa,
					h = 36E5 / Oa,
					C = 864E5 / Oa;
					a = 6048E5 / Oa;
					c = 2592E6 / Oa;
					var p = 31556952E3 / Oa,
					o = [["second", E, [1, 2, 5, 10, 15, 30]], ["minute", J, [1, 2, 5, 10, 15, 30]], ["hour", h, [1, 2, 3, 4, 6, 8, 12]], ["day", C, [1, 2]], ["week", a, [1, 2]], ["month", c, [1, 2, 3, 4, 6]], ["year", p, null]],
					t = o[6],
					z = t[1],
					q = t[2];
					for (b = 0; b < o.length; b++) if (t = o[b], z = t[1], q = t[2], o[b + 1] && K <= (z * q[q.length - 1] + o[b + 1][1]) / 2) break;
					z == p && K < 5 * z && (q = [1, 2, 5]);
					o = g(K / z, q);
					q = new Date(V * Oa);
					q.setMilliseconds(0);
					z >= E && q.setSeconds(z >= J ? 0: o * ha(q.getSeconds() / o));
					if (z >= J) q[ec](z >= h ? 0: o * ha(q[Ib]() / o));
					if (z >= h) q[fc](z >= C ? 0: o * ha(q[Jb]() / o));
					if (z >= C) q[Lb](z >= c ? 1: o * ha(q[pb]() / o));
					z >= c && (q[gc](z >= p ? 0: o * ha(q[xb]() / o)), l = q[yb]());
					z >= p && (l -= l % o, q[hc](l));
					z == a && q[Lb](q[pb]() - q[Kb]() + e.startOfWeek);
					b = 1;
					l = q[yb]();
					E = q.getTime() / Oa;
					J = q[xb]();
					for (h = q[pb](); E < X && b < oa;) ba.push(E),
					z == p ? E = wb(l + b * o, 0) / Oa: z == c ? E = wb(l, J + b * o) / Oa: ! s && (z == C || z == a) ? E = wb(l, J, h + b * o * (z == C ? 1: 7)) : E += z * o,
					b++;
					ba.push(E);
					Gb = e.dateTimeLabelFormats[t[0]]
				} else {
					b = ha(V / K) * K;
					l = gb(X / K) * K;
					ba = [];
					for (b = d(b); b <= l;) ba.push(b),
					b = d(b + K)
				}
				if (!Qa) {
					if (Fa || H && i.hasColumn) {
						l = (Fa ? 1: K) * 0.5;
						if (Fa || ! n(j(e.min, Ha))) V -= l;
						if (Fa || ! n(j(e.max, Ya))) X += l
					}
					l = ba[0];
					b = ba[ba.length - 1];
					e.startOnTick ? V = l: V > l && ba.shift();
					e.endOnTick ? X = b: X < b && ba.pop();
					Xa || (Xa = {
						x: 0,
						y: 0
					});
					if (!R && ba.length > Xa[I]) Xa[I] = ba.length
				}
			}
			function C() {
				var a, i;
				aa = V;
				mc = X;
				s();
				f();
				na = w;
				w = D / (X - V || 1);
				if (!H) for (a in z) for (i in z[a]) z[a][i].cum = z[a][i].total;
				if (!fa.isDirty) fa.isDirty = V != aa || X != mc
			}
			function E(a) {
				a = (new c(a)).render();
				Ja.push(a);
				return a
			}
			function J() {
				var a = e.title,
				s = e.alternateGridColor,
				g = e.lineWidth,
				d, j, f = i.hasRendered,
				C = f && n(aa) && ! isNaN(aa);
				d = F.length && n(V) && n(X);
				D = m ? oa: ea;
				w = D / (X - V || 1);
				Wa = m ? O: ga;
				if (d || Qa) {
					if (Ka && ! Fa) for (d = V + (ba[0] - V) % Ka; d <= X; d += Ka) W[d] || (W[d] = new l(d, true)),
					C && W[d].isNew && W[d].render(null, true),
					W[d].isActive = true,
					W[d].render();
					y(ba, function(a, i) {
						if (!Qa || a >= V && a <= X) C && P[a].isNew && P[a].render(i, true),
						P[a].isActive = true,
						P[a].render(i)
					});
					s && y(ba, function(a, i) {
						if (i % 2 === 0 && a < X) Y[a] || (Y[a] = new c),
						Y[a].options = {
							from: a,
							to: ba[i + 1] !== ya ? ba[i + 1] : X,
							color: s
						},
						Y[a].render(),
						Y[a].isActive = true
					});
					f || y((e.plotLines || []).concat(e.plotBands || []), function(a) {
						Ja.push((new c(a)).render())
					})
				}
				y([P, W, Y], function(a) {
					for (var i in a) a[i].isActive ? a[i].isActive = false: (a[i].destroy(), delete a[i])
				});
				g && (d = O + (o ? oa: 0) + u, j = ua - ga - (o ? ea: 0) + u, d = S.crispLine([Ca, m ? O: d, m ? j: T, ma, m ? Aa - ja: d, m ? j: ua - ga], g), A ? A.animate({
					d: d
				}) : A = S.path(d).attr({
					stroke: e.lineColor,
					"stroke-width": g,
					zIndex: 7
				}).add());
				fa.axisTitle && (d = m ? O: T, g = b(a.style.fontSize || 12), d = {
					low: d + (m ? 0: D),
					middle: d + D / 2,
					high: d + (m ? D: 0)
				} [a.align], g = (m ? T + ea: O) + (m ? 1: - 1) * (o ? - 1: 1) * ka + (t == 2 ? g: 0), fa.axisTitle[f ? "animate": "attr"]({
					x: m ? d: g + (o ? oa: 0) + u + (a.x || 0),
					y: m ? g - (o ? ea: 0) + u: d + (a.y || 0)
				}));
				fa.isDirty = false
			}
			function p(a) {
				for (var i = 0; i < Ja.length; i++) Ja[i].id == a && Ja[i].destroy()
			}
			var H = e.isX,
			o = e.opposite,
			m = qa ? ! H: H,
			t = m ? o ? 0: 2: o ? 1: 3,
			z = {},
			e = ia(H ? zb: Mb, [oc, pc, ic, qc][t], e),
			fa = this,
			R = e.type == "datetime",
			u = e.offset || 0,
			I = H ? "x": "y",
			D,
			w,
			na,
			Wa = m ? O: ga,
			ca,
			mb,
			Ba,
			nb,
			A,
			v,
			Ga,
			F,
			Ha,
			Ya,
			X = null,
			V = null,
			aa,
			mc,
			L = e.minPadding,
			M = e.maxPadding,
			Qa = n(e.linkedTo),
			eb,
			ob,
			Ia,
			Q = e.events,
			Ub,
			Ja = [],
			K,
			Ka,
			U,
			ba,
			P = {},
			W = {},
			Y = {},
			Z,
			da,
			ka,
			Gb,
			Fa = e.categories,
			wa = e.labels.formatter || function() {
				var a = this.value;
				return Gb ? Ab(Gb, a) : K % 1E6 === 0 ? a / 1E6 + "M": K % 1E3 === 0 ? a / 1E3 + "k": ! Fa && a >= 1E3 ? Ma(a, 0) : a
			},
			xa = m && e.labels.staggerLines,
			ra = e.reversed,
			sa = Fa && e.tickmarkPlacement == "between" ? 0.5: 0;
			l.prototype = {
				addLabel: function() {
					var i = this.pos,
					l = e.labels,
					b = ! (i == V && ! j(e.showFirstLabel, 1) || i == X && ! j(e.showLastLabel, 0)),
					c,
					s = this.label,
					i = wa.call({
						isFirst: i == ba[0],
						isLast: i == ba[ba.length - 1],
						dateTimeLabelFormat: Gb,
						value: Fa && Fa[i] ? Fa[i] : i
					});
					c = c && {
						width: c - 2 * (l.padding || 10) + Ea
					};
					s === ya ? this.label = n(i) && b && l.enabled ? S.text(i, 0, 0).attr({
						align: l.align,
						rotation: l.rotation
					}).css(a(c, l.style)).add(Ba) : null: s && s.attr({
						text: i
					}).css(c)
				},
				getLabelSize: function() {
					var a = this.label;
					return a ? (this.labelBBox = a.getBBox())[m ? "height": "width"] : 0
				},
				render: function(a, i) {
					var l = ! this.minor,
					b = this.label,
					c = this.pos,
					s = e.labels,
					g = this.gridLine,
					d = l ? e.gridLineWidth: e.minorGridLineWidth,
					j = l ? e.gridLineColor: e.minorGridLineColor,
					f = l ? e.gridLineDashStyle: e.minorGridLineDashStyle,
					C = this.mark,
					E = l ? e.tickLength: e.minorTickLength,
					J = l ? e.tickWidth: e.minorTickWidth || 0,
					h = l ? e.tickColor: e.minorTickColor,
					p = l ? e.tickPosition: e.minorTickPosition,
					l = s.step,
					H = i && Za || ua,
					z;
					z = m ? ca(c + sa, null, null, i) + Wa: O + u + (o ? (i && cb || Aa) - ja - O: 0);
					H = m ? H - ga + u - (o ? ea: 0) : H - ca(c + sa, null, null, i) - Wa;
					if (d) {
						c = mb(c + sa, d, i);
						if (g === ya) {
							g = {
								stroke: j,
								"stroke-width": d
							};
							if (f) g.dashstyle = f;
							this.gridLine = g = d ? S.path(c).attr(g).add(nb) : null
						}
						g && c && g.animate({
							d: c
						})
					}
					if (J) p == "inside" && (E = - E),
					o && (E = - E),
					d = S.crispLine([Ca, z, H, ma, z + (m ? 0: - E), H + (m ? E: 0)], J),
					C ? C.animate({
						d: d
					}) : this.mark = S.path(d).attr({
						stroke: h,
						"stroke-width": J
					}).add(Ba);
					if (b) {
						z = z + s.x - (sa && m ? sa * w * (ra ? - 1: 1) : 0);
						H = H + s.y - (sa && ! m ? sa * w * (ra ? 1: - 1) : 0);
						n(s.y) || (H += parseInt(b.styles.lineHeight) * 0.9 - b.getBBox().height / 2);
						xa && (H += a % xa * 16);
						if (l) b[a % l ? "hide": "show"]();
						b[this.isNew ? "attr": "animate"]({
							x: z,
							y: H
						})
					}
					this.isNew = false
				},
				destroy: function() {
					for (var a in this) this[a] && this[a].destroy && this[a].destroy()
				}
			};
			c.prototype = {
				render: function() {
					var a = this,
					i = a.options,
					e = i.label,
					l = a.label,
					b = i.width,
					c = i.to,
					s, g = i.from,
					d = i.dashStyle,
					j = a.svgElem,
					f = [],
					C,
					E,
					J = i.color;
					E = i.zIndex;
					var h = i.events;
					if (b) {
						if (f = mb(i.value, b), i = {
							stroke: J,
							"stroke-width": b
						},
						d) i.dashstyle = d
					} else if (n(g) && n(c)) g = G(g, V),
					c = Da(c, X),
					s = mb(c),
					(f = mb(g)) && s ? f.push(s[4], s[5], s[1], s[2]) : f = null,
					i = {
						fill: J
					};
					else return;
					if (n(E)) i.zIndex = E;
					if (j) f ? j.animate({
						d: f
					},
					null, j.onGetPath) : (j.hide(), j.onGetPath = function() {
						j.show()
					});
					else if (f && f.length && (a.svgElem = j = S.path(f).attr(i).add(), h)) for (C in d = function(i) {
						j.on(i, function(e) {
							h[i].apply(a, [e])
						})
					},
					h) d(C);
					if (e && n(e.text) && f && f.length && oa > 0 && ea > 0) {
						e = ia({
							align: m && s && "center",
							x: m ? ! s && 4: 10,
							verticalAlign: ! m && s && "middle",
							y: m ? s ? 16: 10: s ? 6: - 4,
							rotation: m && ! s && 90
						},
						e);
						if (!l) a.label = l = S.text(e.text, 0, 0).attr({
							align: e.textAlign || e.align,
							rotation: e.rotation,
							zIndex: E
						}).css(e.style).add();
						s = [f[1], f[4], f[6] || f[1]];
						f = [f[2], f[5], f[7] || f[2]];
						C = Da.apply(N, s);
						E = Da.apply(N, f);
						l.align(e, false, {
							x: C,
							y: E,
							width: G.apply(N, s) - C,
							height: G.apply(N, f) - E
						});
						l.show()
					} else l && l.hide();
					return a
				},
				destroy: function() {
					for (var a in this) this[a] && this[a].destroy && this[a].destroy(),
					delete this[a];
					h(Ja, this)
				}
			};
			ca = function(a, i, e, l) {
				var b = 1,
				c = 0,
				s = l ? na: w,
				l = l ? aa: V;
				s || (s = w);
				e && (b *= - 1, c = D);
				ra && (b *= - 1, c -= b * D);
				i ? (ra && (a = D - a), a = a / s + l) : a = b * (a - l) * s + c;
				return a
			};
			mb = function(a, i, e) {
				var l, b, c, a = ca(a, null, null, e),
				s = e && Za || ua,
				g = e && cb || Aa,
				d,
				e = b = x(a + Wa);
				l = c = x(s - a - Wa);
				if (isNaN(a)) d = true;
				else if (m) {
					if (l = T, c = s - ga, e < O || e > O + oa) d = true
				} else if (e = O, b = g - ja, l < T || l > T + ea) d = true;
				return d ? null: S.crispLine([Ca, e, l, ma, b, c], i || 0)
			};
			qa && H && ra === ya && (ra = true);
			a(fa, {
				addPlotBand: E,
				addPlotLine: E,
				adjustTickAmount: function() {
					if (Xa && ! R && ! Fa && ! Qa) {
						var a = Z,
						i = ba.length;
						Z = Xa[I];
						if (i < Z) {
							for (; ba.length < Z;) ba.push(d(ba[ba.length - 1] + K));
							w *= (i - 1) / (Z - 1);
							X = ba[ba.length - 1]
						}
						if (n(a) && Z != a) fa.isDirty = true
					}
				},
				categories: Fa,
				getExtremes: function() {
					return {
						min: V,
						max: X,
						dataMin: v,
						dataMax: Ga
					}
				},
				getPlotLinePath: mb,
				getThreshold: function(a) {
					V > a ? a = V: X < a && (a = X);
					return ca(a, 0, 1)
				},
				isXAxis: H,
				options: e,
				plotLinesAndBands: Ja,
				getOffset: function() {
					var a = F.length && n(V) && n(X),
					i = 0,
					b = 0,
					c = e.title,
					s = e.labels,
					d = [ - 1, 1, 1, - 1][t];
					Ba || (Ba = S.g("axis").attr({
						zIndex: 7
					}).add(), nb = S.g("grid").attr({
						zIndex: 1
					}).add());
					da = 0;
					if (a || Qa) y(ba, function(a) {
						P[a] ? P[a].addLabel() : P[a] = new l(a);
						if (t === 0 || t == 2 || {
							1: "left",
							3: "right"
						} [t] == s.align) da = G(P[a].getLabelSize(), da)
					}),
					xa && (da += (xa - 1) * 16);
					else for (var g in P) P[g].destroy(),
					delete P[g];
					if (c && c.text) {
						if (!fa.axisTitle) fa.axisTitle = S.text(c.text, 0, 0).attr({
							zIndex: 7,
							rotation: c.rotation || 0,
							align: c.textAlign || {
								low: "left",
								middle: "center",
								high: "right"
							} [c.align]
						}).css(c.style).add();
						i = fa.axisTitle.getBBox()[m ? "height": "width"];
						b = j(c.margin, m ? 5: 10)
					}
					u = d * (e.offset || pa[t]);
					ka = da + (t != 2 && da && d * e.labels[m ? "y": "x"]) + b;
					pa[t] = G(pa[t], ka + i + d * u)
				},
				render: J,
				setCategories: function(a, e) {
					fa.categories = Fa = a;
					y(F, function(a) {
						a.translate();
						a.setTooltipPoints(true)
					});
					fa.isDirty = true;
					j(e, true) && i.redraw()
				},
				setExtremes: function(a, e, l, b) {
					q(b, i);
					l = j(l, true);
					ta(fa, "setExtremes", {
						min: a,
						max: e
					},
					function() {
						Ha = a;
						Ya = e;
						l && i.redraw()
					})
				},
				setScale: C,
				setTickPositions: f,
				translate: ca,
				redraw: function() {
					hb.resetTracker && hb.resetTracker();
					J();
					y(Ja, function(a) {
						a.render()
					});
					y(F, function(a) {
						a.isDirty = true
					})
				},
				removePlotBand: p,
				removePlotLine: p,
				reversed: ra,
				stacks: z
			});
			for (Ub in Q) va(fa, Ub, Q[Ub]);
			C()
		}
		function s() {
			var a = {};
			return {
				add: function(e, l, b, c) {
					a[e] || (l = S.text(l, 0, 0).css(i.toolbar.itemStyle).align({
						align: "right",
						x: - ja - 20,
						y: T + 30
					}).on("click", c).attr({
						align: "right",
						zIndex: 20
					}).add(), a[e] = l)
				},
				remove: function(i) {
					aa(a[i].element);
					a[i] = null
				}
			}
		}
		function f(a) {
			function i() {
				var a = this.points || p(this),
				e = a[0].series.xAxis,
				l = this.x,
				e = e && e.options.type == "datetime",
				b = c(l) || e,
				s;
				s = b ? ['<span style="font-size: 10px">', e ? Ab("%A, %b %e, %Y", l) : l, "</span><br/>"] : [];
				y(a, function(a) {
					s.push(a.point.tooltipFormatter(b))
				});
				return s.join("")
			}
			function e(a, i) {
				m = n ? a: (2 * m + a) / 3;
				z = n ? i: (z + i) / 2;
				q.translate(m, z);
				Nb = Y(a - m) > 1 || Y(i - z) > 1 ? function() {
					e(a, i)
				}: null
			}
			function l() {
				if (!n) {
					var a = u.hoverPoints;
					q.hide();
					y(j, function(a) {
						a && a.hide()
					});
					a && y(a, function(a) {
						a.setState()
					});
					u.hoverPoints = null;
					n = true
				}
			}
			var s, d = a.borderWidth,
			g = a.crosshairs,
			j = [],
			C = a.style,
			E = a.shared,
			J = b(C.padding),
			h = d + J,
			n = true,
			H,
			o,
			m = 0,
			z = 0;
			C.padding = 0;
			var q = S.g("tooltip").attr({
				zIndex: 8
			}).add(),
			t = S.rect(h, h, 0, 0, a.borderRadius, d).attr({
				fill: a.backgroundColor,
				"stroke-width": d
			}).add(q).shadow(a.shadow),
			fa = S.text("", J + h, b(C.fontSize) + J + h).attr({
				zIndex: 1
			}).css(C).add(q);
			q.hide();
			return {
				shared: E,
				refresh: function(b) {
					var c, d, f, C = 0,
					m = {},
					z = [];
					f = b.tooltipPos;
					c = a.formatter || i;
					var m = u.hoverPoints,
					R = function(a) {
						return {
							series: a.series,
							point: a,
							x: a.category,
							y: a.y,
							percentage: a.percentage,
							total: a.total || a.stackTotal
						}
					};
					E ? (m && y(m, function(a) {
						a.setState()
					}), u.hoverPoints = b, y(b, function(a) {
						a.setState(Sa);
						C += a.plotY;
						z.push(R(a))
					}), d = b[0].plotX, C = x(C) / b.length, m = {
						x: b[0].category
					},
					m.points = z, b = b[0]) : m = R(b);
					m = c.call(m);
					s = b.series;
					d = E ? d: b.plotX;
					C = E ? C: b.plotY;
					c = x(f ? f[0] : qa ? oa - C: d);
					d = x(f ? f[1] : qa ? ea - d: C);
					f = E || ! b.series.isCartesian || ib(c, d);
					m === false || ! f ? l() : (n && (q.show(), n = false), fa.attr({
						text: m
					}), f = fa.getBBox(), H = f.width, o = f.height, t.attr({
						width: H + 2 * J,
						height: o + 2 * J,
						stroke: a.borderColor || b.color || s.color || "#606060"
					}), c = c - H + O - 25, d = d - o + T + 10, c < 7 && (c = 7, d -= 30), d < 5 ? d = 5: d + o > ua && (d = ua - o - 5), e(x(c - h), x(d - h)));
					if (g) {
						g = p(g);
						d = g.length;
						for (var D; d--;) if (g[d] && (D = b.series[d ? "yAxis": "xAxis"])) if (c = D.getPlotLinePath(b[d ? "y": "x"], 1), j[d]) j[d].attr({
							d: c,
							visibility: Ua
						});
						else {
							f = {
								"stroke-width": g[d].width || 1,
								stroke: g[d].color || "#C0C0C0",
								zIndex: 2
							};
							if (g[d].dashStyle) f.dashstyle = g[d].dashStyle;
							j[d] = S.path(c).attr(f).add()
						}
					}
				},
				hide: l
			}
		}
		function E(i, e) {
			function l(a) {
				var i, a = a || v.event;
				if (!a.target) a.target = a.srcElement;
				i = a.touches ? a.touches.item(0) : a;
				if (a.type != "mousemove" || v.opera) {
					for (var e = K, b = {
						left: e.offsetLeft,
						top: e.offsetTop
					}; e = e.offsetParent;) b.left += e.offsetLeft,
					b.top += e.offsetTop,
					e != A.body && e != A.documentElement && (b.left -= e.scrollLeft, b.top -= e.scrollTop);
					qb = b
				}
				D ? (a.chartX = a.x, a.chartY = a.y) : i.layerX === ya ? (a.chartX = i.pageX - qb.left, a.chartY = i.pageY - qb.top) : (a.chartX = a.layerX, a.chartY = a.layerY);
				return a
			}
			function b(a) {
				var i = {
					xAxis: [],
					yAxis: []
				};
				y(wa, function(e) {
					var l = e.translate,
					b = e.isXAxis;
					i[b ? "xAxis": "yAxis"].push({
						axis: e,
						value: l((qa ? ! b: b) ? a.chartX - O: ea - a.chartY + T, true)
					})
				});
				return i
			}
			function c() {
				var a = i.hoverSeries,
				e = i.hoverPoint;
				e && e.onMouseOut();
				a && a.onMouseOut();
				rb && rb.hide();
				Ob = null
			}
			function s() {
				if (J) {
					var a = {
						xAxis: [],
						yAxis: []
					},
					e = J.getBBox(),
					l = e.x - O,
					b = e.y - T;
					E && (y(wa, function(i) {
						var c = i.translate,
						s = i.isXAxis,
						d = qa ? ! s: s,
						g = c(d ? l: ea - b - e.height, true),
						c = c(d ? l + e.width: ea - b, true);
						a[s ? "xAxis": "yAxis"].push({
							axis: i,
							min: Da(g, c),
							max: G(g, c)
						})
					}), ta(i, "selection", a, Pb));
					J = J.destroy()
				}
				i.mouseIsDown = Qb = E = false;
				Va(A, Ha ? "touchend": "mouseup", s)
			}
			var d, j, E, J, h = B.zoomType,
			n = /x/.test(h),
			p = /y/.test(h),
			m = n && ! qa || p && qa,
			o = p && ! qa || n && qa;
			Bb = function() {
				Cb ? (Cb.translate(O, T), qa && Cb.attr({
					width: i.plotWidth,
					height: i.plotHeight
				}).invert()) : i.trackerGroup = Cb = S.g("tracker").attr({
					zIndex: 9
				}).add()
			};
			Bb();
			if (e.enabled) i.tooltip = rb = f(e);
			(function() {
				var f = true;
				K.onmousedown = function(a) {
					a = l(a);
					i.mouseIsDown = Qb = true;
					d = a.chartX;
					j = a.chartY;
					va(A, Ha ? "touchend": "mouseup", s)
				};
				var C = function(a) {
					if (!a || ! (a.touches && a.touches.length > 1)) {
						a = l(a);
						if (!Ha) a.returnValue = false;
						var b = a.chartX,
						s = a.chartY,
						C = ! ib(b - O, s - T);
						Ha && a.type == "touchstart" && (g(a.target, "isTracker") ? i.runTrackerClick || a.preventDefault() : ! ub && ! C && a.preventDefault());
						C && (f || c(), b < O ? b = O: b > O + oa && (b = O + oa), s < T ? s = T: s > T + ea && (s = T + ea));
						if (Qb && a.type != "touchstart") {
							if (E = Math.sqrt(Math.pow(d - b, 2) + Math.pow(j - s, 2)) > 10) {
								if (jb && (n || p) && ib(d - O, j - T)) J || (J = S.rect(O, T, m ? 1: oa, o ? 1: ea, 0).attr({
									fill: "rgba(69,114,167,0.25)",
									zIndex: 7
								}).add());
								J && m && (b -= d, J.attr({
									width: Y(b),
									x: (b > 0 ? 0: b) + d
								}));
								J && o && (s -= j, J.attr({
									height: Y(s),
									y: (s > 0 ? 0: s) + j
								}))
							}
						} else if (!C) {
							var h, s = i.hoverPoint,
							b = i.hoverSeries,
							H, z, q = Aa,
							t = qa ? a.chartY: a.chartX - O;
							if (rb && e.shared) {
								h = [];
								H = la.length;
								for (z = 0; z < H; z++) if (la[z].visible && la[z].tooltipPoints.length) a = la[z].tooltipPoints[t],
								a._dist = Y(t - a.plotX),
								q = Da(q, a._dist),
								h.push(a);
								for (H = h.length; H--;) h[H]._dist > q && h.splice(H, 1);
								if (h.length && h[0].plotX != Ob) rb.refresh(h),
								Ob = h[0].plotX
							}
							b && b.tracker && (a = b.tooltipPoints[t]) && a != s && a.onMouseOver()
						}
						return (f = C) || ! jb
					}
				};
				K.onmousemove = C;
				va(K, "mouseleave", c);
				K.ontouchstart = function(a) {
					if (n || p) K.onmousedown(a);
					C(a)
				};
				K.ontouchmove = C;
				K.ontouchend = function() {
					E && c()
				};
				K.onclick = function(e) {
					var c = i.hoverPoint,
					e = l(e);
					e.cancelBubble = true;
					if (!E) if (c && g(e.target, "isTracker")) {
						var s = c.plotX,
						d = c.plotY;
						a(c, {
							pageX: qb.left + O + (qa ? oa - d: s),
							pageY: qb.top + T + (qa ? ea - s: d)
						});
						ta(c.series, "click", a(e, {
							point: c
						}));
						c.firePointEvent("click", e)
					} else a(e, b(e)),
					ib(e.chartX - O, e.chartY - T) && ta(i, "click", e);
					E = false
				}
			})();
			jc = setInterval(function() {
				Nb && Nb()
			},
			32);
			a(this, {
				zoomX: n,
				zoomY: p,
				resetTracker: c
			})
		}
		function J(a) {
			var i = a.type || B.type || B.defaultSeriesType,
			e = Pa[i],
			l = u.hasRendered;
			if (l) if (qa && i == "column") e = Pa.bar;
			else if (!qa && i == "bar") e = Pa.column;
			i = new e;
			i.init(u, a); ! l && i.inverted && (qa = true);
			if (i.isCartesian) jb = i.isCartesian;
			la.push(i);
			return i
		}
		function H() {
			B.alignTicks !== false && y(wa, function(a) {
				a.adjustTickAmount()
			});
			Xa = null
		}
		function o(a) {
			var i = u.isDirtyLegend,
			e, l = u.isDirtyBox,
			b = la.length,
			c = b,
			s = u.clipRect;
			for (q(a, u); c--;) if (a = la[c], a.isDirty && a.options.stacking) {
				e = true;
				break
			}
			if (e) for (c = b; c--;) if (a = la[c], a.options.stacking) a.isDirty = true;
			y(la, function(a) {
				a.isDirty && (a.cleanData(), a.getSegments(), a.options.legendType == "point" && (i = true))
			});
			if (i && Rb.renderLegend) Rb.renderLegend(),
			u.isDirtyLegend = false;
			jb && (Db || (Xa = null, y(wa, function(a) {
				a.setScale()
			})), H(), sb(), y(wa, function(a) {
				if (a.isDirty || l) a.redraw(),
				l = true
			}));
			l && (Sb(), Bb(), s && (Eb(s), s.animate({
				width: u.plotSizeX,
				height: u.plotSizeY
			})));
			y(la, function(a) {
				a.isDirty && a.visible && (!a.isCartesian || a.xAxis) && a.redraw()
			});
			hb && hb.resetTracker && hb.resetTracker();
			ta(u, "redraw")
		}
		function z() {
			var a = i.xAxis || {},
			l = i.yAxis || {},
			b, a = p(a);
			y(a, function(a, i) {
				a.index = i;
				a.isX = true
			});
			l = p(l);
			y(l, function(a, i) {
				a.index = i
			});
			wa = a.concat(l);
			u.xAxis = [];
			u.yAxis = [];
			wa = kb(wa, function(a) {
				b = new e(u, a);
				u[b.isXAxis ? "xAxis": "yAxis"].push(b);
				return b
			});
			H()
		}
		function R(a, e) {
			Z = ia(i.title, a);
			da = ia(i.subtitle, e);
			y([["title", a, Z], ["subtitle", e, da]], function(a) {
				var i = a[0],
				e = u[i],
				l = a[1],
				a = a[2];
				e && l && (e.destroy(), e = null);
				a && a.text && ! e && (u[i] = S.text(a.text, 0, 0).attr({
					align: a.align,
					"class": "highcharts-" + i,
					zIndex: 1
				}).css(a.style).add().align(a, false, P))
			})
		}
		function I() {
			ra = B.renderTo;
			sa = db + Qa++;
			c(ra) && (ra = A.getElementById(ra));
			ra.innerHTML = "";
			ra.offsetWidth || (ka = ra.cloneNode(0), m(ka, {
				position: lb,
				top: "-9999px",
				display: ""
			}), A.body.appendChild(ka));
			La = (ka || ra).offsetWidth;
			Ta = (ka || ra).offsetHeight;
			u.chartWidth = Aa = B.width || La || 600;
			u.chartHeight = ua = B.height || (Ta > 19 ? Ta: 400);
			u.container = K = t($a, {
				className: "highcharts-container" + (B.className ? " " + B.className: ""),
				id: sa
			},
			a({
				position: kc,
				overflow: Ra,
				width: Aa + Ea,
				height: ua + Ea,
				textAlign: "left"
			},
			B.style), ka || ra);
			u.renderer = S = B.renderer == "SVG" ? new Fb(K, Aa, ua) : new lc(K, Aa, ua);
			var i, e;
			/Firefox/.test(U) && K.getBoundingClientRect && (i = function() {
				m(K, {
					left: 0,
					top: 0
				});
				e = K.getBoundingClientRect();
				m(K, {
					left: - e.left % 1 + Ea,
					top: - e.top % 1 + Ea
				})
			},
			i(), va(v, "resize", i), va(u, "destroy", function() {
				Va(v, "resize", i)
			}))
		}
		function w() {
			function a() {
				var e = B.width || ra.offsetWidth,
				l = B.height || ra.offsetHeight;
				if (e && l) {
					if (e != La || l != Ta) clearTimeout(i),
					i = setTimeout(function() {
						Tb(e, l, false)
					},
					100);
					La = e;
					Ta = l
				}
			}
			var i;
			va(window, "resize", a);
			va(u, "destroy", function() {
				Va(window, "resize", a)
			})
		}
		function Ba() {
			var e = i.labels,
			l = i.credits,
			c;
			R();
			Rb = u.legend = new dc(u);
			sb();
			y(wa, function(a) {
				a.setTickPositions(true)
			});
			H();
			sb();
			Sb();
			jb && y(wa, function(a) {
				a.render()
			});
			if (!u.seriesGroup) u.seriesGroup = S.g("series-group").attr({
				zIndex: 3
			}).add();
			y(la, function(a) {
				a.translate();
				a.setTooltipPoints();
				a.render()
			});
			e.items && y(e.items, function() {
				var i = a(e.style, this.style),
				l = b(i.left) + O,
				c = b(i.top) + T + 12;
				delete i.left;
				delete i.top;
				S.text(this.html, l, c).attr({
					zIndex: 2
				}).css(i).add()
			});
			if (!u.toolbar) u.toolbar = s(u);
			if (l.enabled && ! u.credits) c = l.href,
			S.text(l.text, 0, 0).on("click", function() {
				if (c) location.href = c
			}).attr({
				align: l.position.align,
				zIndex: 8
			}).css(l.style).add().align(l.position);
			Bb();
			u.hasRendered = true;
			ka && (ra.appendChild(K), aa(ka))
		}
		function F() {
			var a = la.length,
			i = K && K.parentNode;
			ta(u, "destroy");
			Va(v, "unload", F);
			Va(u);
			for (y(wa, function(a) {
				Va(a)
			}); a--;) la[a].destroy();
			K.innerHTML = "";
			Va(K);
			i && i.removeChild(K);
			K = null;
			S.alignedObjects = null;
			clearInterval(jc);
			for (a in u) delete u[a]
		}
		function nb() { ! ca && ! v.parent && A.readyState != "complete" ? A.attachEvent("onreadystatechange", function() {
				A.detachEvent("onreadystatechange", nb);
				nb()
			}) : (I(), Vb(), Wb(), y(i.series || [], function(a) {
				J(a)
			}), u.inverted = qa = j(qa, i.chart.inverted), z(), u.render = Ba, u.tracker = hb = new E(u, i.tooltip), Ba(), ta(u, "load"), l && l.apply(u, [u]), y(u.callbacks, function(a) {
				a.apply(u, [u])
			}))
		}
		zb = ia(zb, za.xAxis);
		Mb = ia(Mb, za.yAxis);
		za.xAxis = za.yAxis = null;
		var i = ia(za, i),
		B = i.chart,
		na = B.margin,
		na = d(na) ? na: [na, na, na, na],
		eb = j(B.marginTop, na[0]),
		ob = j(B.marginRight, na[1]),
		L = j(B.marginBottom, na[2]),
		M = j(B.marginLeft, na[3]),
		Q = B.spacingTop,
		Ja = B.spacingRight,
		Ka = B.spacingBottom,
		W = B.spacingLeft,
		P,
		Z,
		da,
		T,
		ja,
		ga,
		O,
		pa,
		ra,
		ka,
		K,
		sa,
		La,
		Ta,
		Aa,
		ua,
		cb,
		Za,
		Xb,
		Yb,
		Zb,
		$b,
		u = this,
		ub = (na = B.events) && !! na.click,
		ac,
		ib,
		rb,
		Qb,
		fb,
		tb,
		bc,
		ea,
		oa,
		hb,
		Cb,
		Bb,
		Rb,
		ab,
		bb,
		qb,
		jb = B.showAxes,
		Db = 0,
		wa = [],
		Xa,
		la = [],
		qa,
		S,
		Nb,
		jc,
		Ob,
		Sb,
		sb,
		Vb,
		Wb,
		Tb,
		Pb,
		nc,
		dc = function(i) {
			function e(a, i) {
				var l = a.legendItem,
				b = a.legendLine,
				c = a.legendSymbol,
				s = p.color,
				d = i ? g.itemStyle.color: s,
				s = i ? a.color: s;
				l && l.css({
					fill: d
				});
				b && b.attr({
					stroke: s
				});
				c && c.attr({
					stroke: s,
					fill: s
				})
			}
			function l(a, i, e) {
				var b = a.legendItem,
				c = a.legendLine,
				s = a.legendSymbol,
				a = a.checkbox;
				b && b.attr({
					x: i,
					y: e
				});
				c && c.translate(i, e - 4);
				s && s.attr({
					x: i + s.xOff,
					y: e + s.yOff
				});
				if (a) a.x = i,
				a.y = e
			}
			function c() {
				y(E, function(a) {
					var i = a.checkbox;
					i && m(i, {
						left: x.attr("translateX") + a.legendItemWidth + i.x - 40 + Ea,
						top: x.attr("translateY") + i.y - 11 + Ea
					})
				})
			}
			function s(a) {
				var i, b, c, d, J, m = a.legendItem;
				d = a.series || a;
				if (!m) {
					J = /^(bar|pie|area|column)$/.test(d.type);
					a.legendItem = m = S.text(g.labelFormatter.call(a), 0, 0).css(a.visible ? h: p).on("mouseover", function() {
						a.setState(Sa);
						m.css(n)
					}).on("mouseout", function() {
						m.css(a.visible ? h: p);
						a.setState()
					}).on("click", function() {
						var i = function() {
							a.setVisible()
						};
						a.firePointEvent ? a.firePointEvent("legendItemClick", null, i) : ta(a, "legendItemClick", null, i)
					}).attr({
						zIndex: 2
					}).add(x);
					if (!J && a.options && a.options.lineWidth) {
						var z = a.options;
						d = {
							"stroke-width": z.lineWidth,
							zIndex: 2
						};
						if (z.dashStyle) d.dashstyle = z.dashStyle;
						a.legendLine = S.path([Ca, - f - C, 0, ma, - C, 0]).attr(d).add(x)
					}
					J ? i = S.rect(b = - f - C, c = - 11, f, 12, 2).attr({
						"stroke-width": 0,
						zIndex: 3
					}).add(x) : a.options && a.options.marker && a.options.marker.enabled && (i = S.symbol(a.symbol, b = - f / 2 - C, c = - 4, a.options.marker.radius).attr(a.pointAttr[xa]).attr({
						zIndex: 3
					}).add(x));
					if (i) i.xOff = b,
					i.yOff = c;
					a.legendSymbol = i;
					e(a, a.visible);
					if (a.options && a.options.showCheckbox) a.checkbox = t("input", {
						type: "checkbox",
						checked: a.selected,
						defaultChecked: a.selected
					},
					g.itemCheckboxStyle, K),
					va(a.checkbox, "click", function(i) {
						ta(a, "checkboxClick", {
							checked: i.target.checked
						},
						function() {
							a.select()
						})
					})
				}
				i = m.getBBox();
				b = a.legendItemWidth = g.itemWidth || f + C + i.width + o;
				D = i.height;
				if (j && fa - q + b > (na || Aa - 2 * H - q)) fa = q,
				R += D;
				u = R;
				l(a, fa, R);
				j ? fa += b: R += D;
				Wa = na || G(j ? fa - q: b, Wa);
				E.push(a)
			}
			function d() {
				fa = q;
				R = z;
				u = Wa = 0;
				E = [];
				x || (x = S.g("legend").attr({
					zIndex: 7
				}).add());
				ca && v.reverse();
				y(v, function(a) {
					a.options.showInLegend && y(a.options.legendType == "point" ? a.data: [a], s)
				});
				ca && v.reverse();
				ab = na || Wa;
				bb = u - z + D;
				if (I || w) ab += 2 * H,
				bb += 2 * H,
				B ? ab > 0 && bb > 0 && B.animate({
					width: ab,
					height: bb
				}) : B = S.rect(0, 0, ab, bb, g.borderRadius, I || 0).attr({
					stroke: g.borderColor,
					"stroke-width": I || 0,
					fill: w || Na
				}).add(x).shadow(g.shadow),
				B[E.length ? "show": "hide"]();
				for (var i = ["left", "right", "top", "bottom"], e, l = 4; l--;) e = i[l],
				J[e] && J[e] != "auto" && (g[l < 2 ? "align": "verticalAlign"] = e, g[l < 2 ? "x": "y"] = b(J[e]) * (l % 2 ? - 1: 1));
				x.align(a(g, {
					width: ab,
					height: bb
				}), true, P);
				Db || c()
			}
			var g = i.options.legend;
			if (g.enabled) {
				var j = g.layout == "horizontal",
				f = g.symbolWidth,
				C = g.symbolPadding,
				E, J = g.style,
				h = g.itemStyle,
				n = g.itemHoverStyle,
				p = g.itemHiddenStyle,
				H = b(J.padding),
				o = 20,
				z = 18,
				q = 4 + H + f + C,
				fa,
				R,
				u,
				D = 0,
				B,
				I = g.borderWidth,
				w = g.backgroundColor,
				x,
				Wa,
				na = g.width,
				v = i.series,
				ca = g.reversed;
				d();
				va(i, "endResize", c);
				return {
					colorizeItem: e,
					destroyItem: function(a) {
						var i = a.checkbox;
						y(["legendItem", "legendLine", "legendSymbol"], function(i) {
							a[i] && a[i].destroy()
						});
						i && aa(a.checkbox)
					},
					renderLegend: d
				}
			}
		};
		ib = function(a, i) {
			return a >= 0 && a <= oa && i >= 0 && i <= ea
		};
		nc = function() {
			ta(u, "selection", {
				resetSelection: true
			},
			Pb);
			u.toolbar.remove("zoom")
		};
		Pb = function(a) {
			var i = za.lang,
			e = u.pointCount < 100;
			u.toolbar.add("zoom", i.resetZoom, i.resetZoomTitle, nc); ! a || a.resetSelection ? y(wa, function(a) {
				a.setExtremes(null, null, false, e)
			}) : y(a.xAxis.concat(a.yAxis), function(a) {
				var i = a.axis;
				u.tracker[i.isXAxis ? "zoomX": "zoomY"] && i.setExtremes(a.min, a.max, false, e)
			});
			o()
		};
		sb = function() {
			var a = i.legend,
			e = j(a.margin, 10),
			l = a.x,
			b = a.y,
			c = a.align,
			s = a.verticalAlign,
			d;
			Vb();
			if ((u.title || u.subtitle) && ! n(eb)) if (d = G(u.title && ! Z.floating && ! Z.verticalAlign && Z.y || 0, u.subtitle && ! da.floating && ! da.verticalAlign && da.y || 0)) T = G(T, d + j(Z.margin, 15) + Q);
			a.enabled && ! a.floating && (c == "right" ? n(ob) || (ja = G(ja, ab - l + e + Ja)) : c == "left" ? n(M) || (O = G(O, ab + l + e + W)) : s == "top" ? n(eb) || (T = G(T, bb + b + e + Q)) : s == "bottom" && (n(L) || (ga = G(ga, bb - b + e + Ka))));
			jb && y(wa, function(a) {
				a.getOffset()
			});
			n(M) || (O += pa[3]);
			n(eb) || (T += pa[0]);
			n(L) || (ga += pa[2]);
			n(ob) || (ja += pa[1]);
			Wb()
		};
		Tb = function(a, i, e) {
			var l = u.title,
			b = u.subtitle;
			Db += 1;
			q(e, u);
			Za = ua;
			cb = Aa;
			Aa = x(a);
			ua = x(i);
			m(K, {
				width: Aa + Ea,
				height: ua + Ea
			});
			S.setSize(Aa, ua, e);
			oa = Aa - O - ja;
			ea = ua - T - ga;
			Xa = null;
			y(wa, function(a) {
				a.isDirty = true;
				a.setScale()
			});
			y(la, function(a) {
				a.isDirty = true
			});
			u.isDirtyLegend = true;
			u.isDirtyBox = true;
			sb();
			l && l.align(null, null, P);
			b && b.align(null, null, P);
			o(e);
			Za = null;
			ta(u, "resize");
			setTimeout(function() {
				ta(u, "endResize", null, function() {
					Db -= 1
				})
			},
			vb && vb.duration || 500)
		};
		Wb = function() {
			u.plotLeft = O = x(O);
			u.plotTop = T = x(T);
			u.plotWidth = oa = x(Aa - O - ja);
			u.plotHeight = ea = x(ua - T - ga);
			u.plotSizeX = qa ? ea: oa;
			u.plotSizeY = qa ? oa: ea;
			P = {
				x: W,
				y: Q,
				width: Aa - W - Ja,
				height: ua - Q - Ka
			}
		};
		Vb = function() {
			T = j(eb, Q);
			ja = j(ob, Ja);
			ga = j(L, Ka);
			O = j(M, W);
			pa = [0, 0, 0, 0]
		};
		Sb = function() {
			var a = B.borderWidth || 0,
			i = B.backgroundColor,
			e = B.plotBackgroundColor,
			l = B.plotBackgroundImage,
			b, c = {
				x: O,
				y: T,
				width: oa,
				height: ea
			};
			b = a + (B.shadow ? 8: 0);
			if (a || i) Xb ? Xb.animate({
				width: Aa - b,
				height: ua - b
			}) : Xb = S.rect(b / 2, b / 2, Aa - b, ua - b, B.borderRadius, a).attr({
				stroke: B.borderColor,
				"stroke-width": a,
				fill: i || Na
			}).add().shadow(B.shadow);
			e && (Yb ? Yb.animate(c) : Yb = S.rect(O, T, oa, ea, 0).attr({
				fill: e
			}).add().shadow(B.plotShadow));
			l && (Zb ? Zb.animate(c) : Zb = S.image(l, O, T, oa, ea).add());
			B.plotBorderWidth && ($b ? $b.animate(c) : $b = S.rect(O, T, oa, ea, 0, B.plotBorderWidth).attr({
				stroke: B.plotBorderColor,
				"stroke-width": B.plotBorderWidth,
				zIndex: 4
			}).add());
			u.isDirtyBox = false
		};
		Ya = Ia = 0;
		va(v, "unload", F);
		B.reflow !== false && va(u, "load", w);
		if (na) for (ac in na) va(u, ac, na[ac]);
		u.options = i;
		u.series = la;
		u.addSeries = function(a, i, e) {
			var l;
			a && (q(e, u), i = j(i, true), ta(u, "addSeries", {
				options: a
			},
			function() {
				l = J(a);
				l.isDirty = true;
				u.isDirtyLegend = true;
				i && u.redraw()
			}));
			return l
		};
		u.animation = j(B.animation, true);
		u.destroy = F;
		u.get = function(a) {
			var i, e, l;
			for (i = 0; i < wa.length; i++) if (wa[i].options.id == a) return wa[i];
			for (i = 0; i < la.length; i++) if (la[i].options.id == a) return la[i];
			for (i = 0; i < la.length; i++) {
				l = la[i].data;
				for (e = 0; e < l.length; e++) if (l[e].id == a) return l[e]
			}
			return null
		};
		u.getSelectedPoints = function() {
			var a = [];
			y(la, function(i) {
				a = a.concat(cc(i.data, function(a) {
					return a.selected
				}))
			});
			return a
		};
		u.getSelectedSeries = function() {
			return cc(la, function(a) {
				return a.selected
			})
		};
		u.hideLoading = function() {
			Hb(fb, {
				opacity: 0
			},
			{
				duration: i.loading.hideDuration,
				complete: function() {
					m(fb, {
						display: Na
					})
				}
			});
			bc = false
		};
		u.isInsidePlot = ib;
		u.redraw = o;
		u.setSize = Tb;
		u.setTitle = R;
		u.showLoading = function(e) {
			var l = i.loading;
			fb || (fb = t($a, {
				className: "highcharts-loading"
			},
			a(l.style, {
				left: O + Ea,
				top: T + Ea,
				width: oa + Ea,
				height: ea + Ea,
				zIndex: 10,
				display: Na
			}), K), tb = t("span", null, l.labelStyle, fb));
			tb.innerHTML = e || i.lang.loading;
			bc || (m(fb, {
				opacity: 0,
				display: ""
			}), Hb(fb, {
				opacity: l.style.opacity
			},
			{
				duration: l.showDuration
			}), bc = true)
		};
		u.pointCount = 0;
		nb()
	}
	var A = document,
	v = window,
	N = Math,
	x = N.round,
	ha = N.floor,
	gb = N.ceil,
	G = N.max,
	Da = N.min,
	Y = N.abs,
	Z = N.cos,
	da = N.sin,
	P = N.PI,
	L = P * 2 / 360,
	U = navigator.userAgent,
	D = /msie/i.test(U) && ! v.opera,
	I = A.documentMode == 8,
	Ba = /AppleWebKit/.test(U),
	ca = v.SVGAngle || A.implementation.hasFeature("http://www.w3.org/TR/SVG11/feature#BasicStructure", "1.1"),
	Ha = "ontouchstart" in A.documentElement,
	Ia,
	Ya,
	Ja = {},
	Qa = 0,
	Oa = 1,
	Ka,
	za,
	Ab,
	vb,
	cb,
	ya,
	$a = "div",
	lb = "absolute",
	kc = "relative",
	Ra = "hidden",
	db = "highcharts-",
	Ua = "visible",
	Ea = "px",
	Na = "none",
	Ca = "M",
	ma = "L",
	tb = "rgba(192,192,192," + (ca ? (1.0E-6):0.002) + ")",
	xa = "",
	Sa = "hover",
	wb,
	Ib,
	Jb,
	Kb,
	pb,
	xb,
	yb,
	ec,
	fc,
	Lb,
	gc,
	hc,
	ja = v.HighchartsAdapter,
	sa = ja || {},
	y = sa.each,
	cc = sa.grep,
	kb = sa.map,
	ia = sa.merge,
	ub = sa.hyphenate,
	va = sa.addEvent,
	Va = sa.removeEvent,
	ta = sa.fireEvent,
	Hb = sa.animate,
	Eb = sa.stop,
	Pa = {};
	ja && ja.init && ja.init();
	if (!ja && v.jQuery) {
		var ga = jQuery,
		y = function(a, l) {
			for (var e = 0, b = a.length; e < b; e++) if (l.call(a[e], a[e], e, a) === false) return e
		},
		cc = ga.grep,
		kb = function(a, l) {
			for (var e = [], b = 0, c = a.length; b < c; b++) e[b] = l.call(a[b], a[b], b, a);
			return e
		},
		ia = function() {
			var a = arguments;
			return ga.extend(true, null, a[0], a[1], a[2], a[3])
		},
		ub = function(a) {
			return a.replace(/([A-Z])/g, function(a, i) {
				return "-" + i.toLowerCase()
			})
		},
		va = function(a, l, e) {
			ga(a).bind(l, e)
		},
		Va = function(a, l, e) {
			var b = A.removeEventListener ? "removeEventListener": "detachEvent";
			A[b] && ! a[b] && (a[b] = function() {});
			ga(a).unbind(l, e)
		},
		ta = function(i, l, e, b) {
			var c = ga.Event(l),
			d = "detached" + l;
			a(c, e);
			i[l] && (i[d] = i[l], i[l] = null);
			ga(i).trigger(c);
			i[d] && (i[l] = i[d], i[d] = null);
			b && ! c.isDefaultPrevented() && b(c)
		},
		Hb = function(a, l, e) {
			var b = ga(a);
			if (l.d) a.toD = l.d,
			l.d = 1;
			b.stop();
			b.animate(l, e)
		},
		Eb = function(a) {
			ga(a).stop()
		};
		ga.extend(ga.easing, {
			easeOutQuad: function(a, l, e, b, c) {
				return - b * (l /= c) * (l - 2) + e
			}
		});
		var dc = jQuery.fx.step._default,
		rc = jQuery.fx.prototype.cur;
		ga.fx.step._default = function(a) {
			var l = a.elem;
			l.attr ? l.attr(a.prop, a.now) : dc.apply(this, arguments)
		};
		ga.fx.step.d = function(a) {
			var l = a.elem;
			if (!a.started) {
				var e = cb.init(l, l.d, l.toD);
				a.start = e[0];
				a.end = e[1];
				a.started = true
			}
			l.attr("d", cb.step(a.start, a.end, a.pos, l.toD))
		};
		ga.fx.prototype.cur = function() {
			var a = this.elem;
			return a.attr ? a.attr(this.prop) : rc.apply(this, arguments)
		}
	}
	cb = {
		init: function(a, l, e) {
			var l = l || "",
			b = a.shift,
			c = l.indexOf("C") > - 1,
			d = c ? 7: 3,
			g,
			l = l.split(" "),
			e = [].concat(e),
			f,
			j,
			h = function(a) {
				for (g = a.length; g--;) a[g] == Ca && a.splice(g + 1, 0, a[g + 1], a[g + 2], a[g + 1], a[g + 2])
			};
			c && (h(l), h(e));
			a.isArea && (f = l.splice(l.length - 6, 6), j = e.splice(e.length - 6, 6));
			if (b) e = [].concat(e).splice(0, d).concat(e),
			a.shift = false;
			if (l.length) for (a = e.length; l.length < a;) b = [].concat(l).splice(l.length - d, d),
			c && (b[d - 6] = b[d - 2], b[d - 5] = b[d - 1]),
			l = l.concat(b);
			f && (l = l.concat(f), e = e.concat(j));
			return [l, e]
		},
		step: function(a, l, e, b) {
			var c = [],
			d = a.length;
			if (e == 1) c = b;
			else if (d == l.length && e < 1) for (; d--;) b = parseFloat(a[d]),
			c[d] = isNaN(b) ? a[d] : e * parseFloat(l[d] - b) + b;
			else c = l;
			return c
		}
	};
	ja = {
		enabled: true,
		align: "center",
		x: 0,
		y: 15,
		style: {
			color: "#666",
			fontSize: "11px",
			lineHeight: "14px"
		}
	};
	za = {
		colors: "#4572A7,#AA4643,#89A54E,#80699B,#3D96AE,#DB843D,#92A8CD,#A47D7C,#B5CA92".split(","),
		symbols: ["circle", "diamond", "square", "triangle", "triangle-down"],
		lang: {
			loading: "Loading...",
			months: "January,February,March,April,May,June,July,August,September,October,November,December".split(","),
			weekdays: "Sunday,Monday,Tuesday,Wednesday,Thursday,Friday,Saturday".split(","),
			decimalPoint: ".",
			resetZoom: "Reset zoom",
			resetZoomTitle: "Reset zoom level 1:1",
			thousandsSep: ","
		},
		global: {
			useUTC: true
		},
		chart: {
			borderColor: "#4572A7",
			borderRadius: 5,
			defaultSeriesType: "line",
			ignoreHiddenSeries: true,
			spacingTop: 10,
			spacingRight: 10,
			spacingBottom: 15,
			spacingLeft: 10,
			style: {
				fontFamily: '"Lucida Grande", "Lucida Sans Unicode", Verdana, Arial, Helvetica, sans-serif',
				fontSize: "12px"
			},
			backgroundColor: "#FFFFFF",
			plotBorderColor: "#C0C0C0"
		},
		title: {
			text: "Chart title",
			align: "center",
			y: 15,
			style: {
				color: "#3E576F",
				fontSize: "16px"
			}
		},
		subtitle: {
			text: "",
			align: "center",
			y: 30,
			style: {
				color: "#6D869F"
			}
		},
		plotOptions: {
			line: {
				allowPointSelect: false,
				showCheckbox: false,
				animation: {
					duration: 1E3
				},
				events: {},
				lineWidth: 2,
				shadow: true,
				marker: {
					enabled: true,
					lineWidth: 0,
					radius: 4,
					lineColor: "#FFFFFF",
					states: {
						hover: {},
						select: {
							fillColor: "#FFFFFF",
							lineColor: "#000000",
							lineWidth: 2
						}
					}
				},
				point: {
					events: {}
				},
				dataLabels: ia(ja, {
					enabled: false,
					y: - 6,
					formatter: function() {
						return this.y
					}
				}),
				showInLegend: true,
				states: {
					hover: {
						marker: {}
					},
					select: {
						marker: {}
					}
				},
				stickyTracking: true
			}
		},
		labels: {
			style: {
				position: lb,
				color: "#3E576F"
			}
		},
		legend: {
			enabled: true,
			align: "center",
			layout: "horizontal",
			labelFormatter: function() {
				return this.name
			},
			borderWidth: 1,
			borderColor: "#909090",
			borderRadius: 5,
			shadow: false,
			style: {
				padding: "5px"
			},
			itemStyle: {
				cursor: "pointer",
				color: "#3E576F"
			},
			itemHoverStyle: {
				cursor: "pointer",
				color: "#000000"
			},
			itemHiddenStyle: {
				color: "#C0C0C0"
			},
			itemCheckboxStyle: {
				position: lb,
				width: "13px",
				height: "13px"
			},
			symbolWidth: 16,
			symbolPadding: 5,
			verticalAlign: "bottom",
			x: 0,
			y: 0
		},
		loading: {
			hideDuration: 100,
			labelStyle: {
				fontWeight: "bold",
				position: kc,
				top: "1em"
			},
			showDuration: 100,
			style: {
				position: lb,
				backgroundColor: "white",
				opacity: 0.5,
				textAlign: "center"
			}
		},
		tooltip: {
			enabled: true,
			backgroundColor: "rgba(255, 255, 255, .85)",
			borderWidth: 2,
			borderRadius: 5,
			shadow: true,
			snap: Ha ? 25: 10,
			style: {
				color: "#333333",
				fontSize: "12px",
				padding: "5px",
				whiteSpace: "nowrap"
			}
		},
		toolbar: {
			itemStyle: {
				color: "#4572A7",
				cursor: "pointer"
			}
		},
		credits: {
			enabled: true,
			text: "Highcharts.com",
			href: "http://www.highcharts.com",
			position: {
				align: "right",
				x: - 10,
				verticalAlign: "bottom",
				y: - 5
			},
			style: {
				cursor: "pointer",
				color: "#909090",
				fontSize: "10px"
			}
		}
	};
	var zb = {
		dateTimeLabelFormats: {
			second: "%H:%M:%S",
			minute: "%H:%M",
			hour: "%H:%M",
			day: "%e. %b",
			week: "%e. %b",
			month: "%b '%y",
			year: "%Y"
		},
		endOnTick: false,
		gridLineColor: "#C0C0C0",
		labels: ja,
		lineColor: "#C0D0E0",
		lineWidth: 1,
		max: null,
		min: null,
		minPadding: 0.01,
		maxPadding: 0.01,
		minorGridLineColor: "#E0E0E0",
		minorGridLineWidth: 1,
		minorTickColor: "#A0A0A0",
		minorTickLength: 2,
		minorTickPosition: "outside",
		startOfWeek: 1,
		startOnTick: false,
		tickColor: "#C0D0E0",
		tickLength: 5,
		tickmarkPlacement: "between",
		tickPixelInterval: 100,
		tickPosition: "outside",
		tickWidth: 1,
		title: {
			align: "middle",
			style: {
				color: "#6D869F",
				fontWeight: "bold"
			}
		},
		type: "linear"
	},
	Mb = ia(zb, {
		endOnTick: true,
		gridLineWidth: 1,
		tickPixelInterval: 72,
		showLastLabel: true,
		labels: {
			align: "right",
			x: - 8,
			y: 3
		},
		lineWidth: 0,
		maxPadding: 0.05,
		minPadding: 0.05,
		startOnTick: true,
		tickWidth: 0,
		title: {
			rotation: 270,
			text: "Y-values"
		}
	}),
	qc = {
		labels: {
			align: "right",
			x: - 8,
			y: null
		},
		title: {
			rotation: 270
		}
	},
	pc = {
		labels: {
			align: "left",
			x: 8,
			y: null
		},
		title: {
			rotation: 90
		}
	},
	ic = {
		labels: {
			align: "center",
			x: 0,
			y: 14
		},
		title: {
			rotation: 0
		}
	},
	oc = ia(ic, {
		labels: {
			y: - 5
		}
	}),
	ka = za.plotOptions,
	ja = ka.line;
	ka.spline = ia(ja);
	ka.scatter = ia(ja, {
		lineWidth: 0,
		states: {
			hover: {
				lineWidth: 0
			}
		}
	});
	ka.area = ia(ja, {});
	ka.areaspline = ia(ka.area);
	ka.column = ia(ja, {
		borderColor: "#FFFFFF",
		borderWidth: 1,
		borderRadius: 0,
		groupPadding: 0.2,
		marker: null,
		pointPadding: 0.1,
		minPointLength: 0,
		states: {
			hover: {
				brightness: 0.1,
				shadow: false
			},
			select: {
				color: "#C0C0C0",
				borderColor: "#000000",
				shadow: false
			}
		}
	});
	ka.bar = ia(ka.column, {
		dataLabels: {
			align: "left",
			x: 5,
			y: 0
		}
	});
	ka.pie = ia(ja, {
		borderColor: "#FFFFFF",
		borderWidth: 1,
		center: ["50%", "50%"],
		colorByPoint: true,
		dataLabels: {
			distance: 30,
			enabled: true,
			formatter: function() {
				return this.point.name
			},
			y: 5
		},
		legendType: "point",
		marker: null,
		size: "75%",
		showInLegend: false,
		slicedOffset: 10,
		states: {
			hover: {
				brightness: 0.1,
				shadow: false
			}
		}
	});
	w();
	var La = function(a) {
		var l = [],
		e;
		(function(a) {
			if (e = /rgba\(\s*([0-9]{1,3})\s*,\s*([0-9]{1,3})\s*,\s*([0-9]{1,3})\s*,\s*([0-9]?(?:\.[0-9]+)?)\s*\)/.exec(a)) l = [b(e[1]), b(e[2]), b(e[3]), parseFloat(e[4], 10)];
			else if (e = /#([a-fA-F0-9]{2})([a-fA-F0-9]{2})([a-fA-F0-9]{2})/.exec(a)) l = [b(e[1], 16), b(e[2], 16), b(e[3], 16), 1]
		})(a);
		return {
			get: function(e) {
				return l && ! isNaN(l[0]) ? e == "rgb" ? "rgb(" + l[0] + "," + l[1] + "," + l[2] + ")": e == "a" ? l[3] : "rgba(" + l.join(",") + ")": a
			},
			brighten: function(a) {
				if (f(a) && a !== 0) {
					var i;
					for (i = 0; i < 3; i++) l[i] += b(a * 255),
					l[i] < 0 && (l[i] = 0),
					l[i] > 255 && (l[i] = 255)
				}
				return this
			},
			setOpacity: function(a) {
				l[3] = a;
				return this
			}
		}
	};
	Ab = function(a, l, e) {
		function b(a) {
			return a.toString().replace(/^([0-9])$/, "0$1")
		}
		if (!n(l) || isNaN(l)) return "Invalid date";
		var a = j(a, "%Y-%m-%d %H:%M:%S"),
		l = new Date(l * Oa),
		c = l[Jb](),
		d = l[Kb](),
		g = l[pb](),
		f = l[xb](),
		h = l[yb](),
		p = za.lang,
		m = p.weekdays,
		p = p.months,
		l = {
			a: m[d].substr(0, 3),
			A: m[d],
			d: b(g),
			e: g,
			b: p[f].substr(0, 3),
			B: p[f],
			m: b(f + 1),
			y: h.toString().substr(2, 2),
			Y: h,
			H: b(c),
			I: b(c % 12 || 12),
			l: c % 12 || 12,
			M: b(l[Ib]()),
			p: c < 12 ? "AM": "PM",
			P: c < 12 ? "am": "pm",
			S: b(l.getSeconds())
		},
		o;
		for (o in l) a = a.replace("%" + o, l[o]);
		return e ? a.substr(0, 1).toUpperCase() + a.substr(1) : a
	};
	M.prototype = {
		init: function(a, l) {
			this.element = A.createElementNS("http://www.w3.org/2000/svg", l);
			this.renderer = a
		},
		animate: function(a, l, e) {
			if (l = j(l, vb, true)) {
				l = ia(l);
				if (e) l.complete = e;
				Hb(this, a, l)
			} else this.attr(a),
			e && e()
		},
		attr: function(a, l) {
			var e, s, d, f, j = this.element,
			h = j.nodeName,
			p = this.renderer,
			m, o = this.shadows,
			q, t = this;
			c(a) && n(l) && (e = a, a = {},
			a[e] = l);
			if (c(a)) e = a,
			h == "circle" ? e = {
				x: "cx",
				y: "cy"
			} [e] || e: e == "strokeWidth" && (e = "stroke-width"),
			t = g(j, e) || this[e] || 0,
			e != "d" && e != "visibility" && (t = parseFloat(t));
			else for (e in a) {
				m = false;
				s = a[e];
				if (e == "d") s && s.join && (s = s.join(" ")),
				/(NaN| {2}|^$)/.test(s) && (s = "M 0 0"),
				this.d = s;
				else if (e == "x" && h == "text") {
					for (d = 0; d < j.childNodes.length; d++) f = j.childNodes[d],
					g(f, "x") == g(j, "x") && g(f, "x", s);
					this.rotation && g(j, "transform", "rotate(" + this.rotation + " " + s + " " + b(a.y || g(j, "y")) + ")")
				} else if (e == "fill") s = p.color(s, j, e);
				else if (h == "circle" && (e == "x" || e == "y")) e = {
					x: "cx",
					y: "cy"
				} [e] || e;
				else if (e == "translateX" || e == "translateY" || e == "rotation" || e == "verticalAlign") this[e] = s,
				this.updateTransform(),
				m = true;
				else if (e == "stroke") s = p.color(s, j, e);
				else if (e == "dashstyle") {
					if (e = "stroke-dasharray", s) {
						s = s.toLowerCase().replace("shortdashdotdot", "3,1,1,1,1,1,").replace("shortdashdot", "3,1,1,1").replace("shortdot", "1,1,").replace("shortdash", "3,1,").replace("longdash", "8,3,").replace(/dot/g, "1,3,").replace("dash", "4,3,").replace(/,$/, "").split(",");
						for (d = s.length; d--;) s[d] = b(s[d]) * a["stroke-width"];
						s = s.join(",")
					}
				} else e == "isTracker" ? this[e] = s: e == "width" ? s = b(s) : e == "align" && (e = "text-anchor", s = {
					left: "start",
					center: "middle",
					right: "end"
				} [s]);
				e == "strokeWidth" && (e = "stroke-width");
				Ba && e == "stroke-width" && s === 0 && (s = 1.0E-6);
				this.symbolName && /^(x|y|r|start|end|innerR)/.test(e) && (q || (this.symbolAttr(a), q = true), m = true);
				if (o && /^(width|height|visibility|x|y|d)$/.test(e)) for (d = o.length; d--;) g(o[d], e, s);
				e == "text" ? (this.textStr = s, p.buildText(this)) : m || g(j, e, s)
			}
			return t
		},
		symbolAttr: function(a) {
			this.x = j(a.x, this.x);
			this.y = j(a.y, this.y);
			this.r = j(a.r, this.r);
			this.start = j(a.start, this.start);
			this.end = j(a.end, this.end);
			this.width = j(a.width, this.width);
			this.height = j(a.height, this.height);
			this.innerR = j(a.innerR, this.innerR);
			this.attr({
				d: this.renderer.symbols[this.symbolName](this.x, this.y, this.r, {
					start: this.start,
					end: this.end,
					width: this.width,
					height: this.height,
					innerR: this.innerR
				})
			})
		},
		clip: function(a) {
			return this.attr("clip-path", "url(" + this.renderer.url + "#" + a.id + ")")
		},
		css: function(i) {
			var l = this.element;
			if (i && i.color) i.fill = i.color;
			i = a(this.styles, i);
			D && ! ca ? m(this.element, i) : this.attr({
				style: o(i)
			});
			this.styles = i;
			i.width && l.nodeName == "text" && this.added && this.renderer.buildText(this);
			return this
		},
		on: function(a, l) {
			var e = l;
			Ha && a == "click" && (a = "touchstart", e = function(a) {
				a.preventDefault();
				l()
			});
			this.element["on" + a] = e;
			return this
		},
		translate: function(a, l) {
			return this.attr({
				translateX: a,
				translateY: l
			})
		},
		invert: function() {
			this.inverted = true;
			this.updateTransform();
			return this
		},
		updateTransform: function() {
			var a = this.translateX || 0,
			l = this.translateY || 0,
			e = this.inverted,
			b = this.rotation,
			c = [];
			e && (a += this.attr("width"), l += this.attr("height"));
			(a || l) && c.push("translate(" + a + "," + l + ")");
			e ? c.push("rotate(90) scale(-1,1)") : b && c.push("rotate(" + b + " " + this.x + " " + this.y + ")");
			c.length && g(this.element, "transform", c.join(" "))
		},
		toFront: function() {
			var a = this.element;
			a.parentNode.appendChild(a);
			return this
		},
		align: function(a, l, e) {
			a ? (this.alignOptions = a, this.alignByTranslate = l, e || this.renderer.alignedObjects.push(this)) : (a = this.alignOptions, l = this.alignByTranslate);
			var e = j(e, this.renderer),
			b = a.align,
			c = a.verticalAlign,
			d = (e.x || 0) + (a.x || 0),
			g = (e.y || 0) + (a.y || 0),
			f = {};
			/^(right|center)$/.test(b) && (d += (e.width - (a.width || 0)) / {
				right: 1,
				center: 2
			} [b]);
			f[l ? "translateX": "x"] = d;
			/^(bottom|middle)$/.test(c) && (g += (e.height - (a.height || 0)) / ({
				bottom: 1,
				middle: 2
			} [c] || 1));
			f[l ? "translateY": "y"] = g;
			this[this.placed ? "animate": "attr"](f);
			this.placed = true;
			return this
		},
		getBBox: function() {
			var i, b, e, c = this.rotation,
			d = c * L;
			try {
				i = a({},
				this.element.getBBox())
			} catch(g) {
				i = {
					width: 0,
					height: 0
				}
			}
			b = i.width;
			e = i.height;
			if (c) i.width = Y(e * da(d)) + Y(b * Z(d)),
			i.height = Y(e * Z(d)) + Y(b * da(d));
			return i
		},
		show: function() {
			return this.attr({
				visibility: Ua
			})
		},
		hide: function() {
			return this.attr({
				visibility: Ra
			})
		},
		add: function(a) {
			var l = this.renderer,
			e = a || l,
			c = e.element || l.box,
			d = c.childNodes,
			f = this.element,
			j = g(f, "zIndex"),
			h = this.textStr,
			p;
			this.parentInverted = a && a.inverted;
			if (j) e.handleZ = true,
			j = b(j);
			if (e.handleZ) for (p = 0; p < d.length; p++) if (a = d[p], e = g(a, "zIndex"), a != f && (b(e) > j || ! n(j) && n(e))) return c.insertBefore(f, a),
			this;
			if (h !== void 0) l.buildText(this),
			this.added = true;
			c.appendChild(f);
			return this
		},
		destroy: function() {
			var a = this.element || {},
			b = this.shadows,
			e = a.parentNode,
			c;
			a.onclick = a.onmouseout = a.onmouseover = a.onmousemove = null;
			Eb(this);
			e && e.removeChild(a);
			b && y(b, function(a) { (e = a.parentNode) && e.removeChild(a)
			});
			h(this.renderer.alignedObjects, this);
			for (c in this) delete this[c];
			return null
		},
		empty: function() {
			for (var a = this.element, b = a.childNodes, e = b.length; e--;) a.removeChild(b[e])
		},
		shadow: function(a) {
			var b = [],
			e,
			c = this.element,
			d = this.parentInverted ? "(-1,-1)": "(1,1)";
			if (a) {
				for (a = 1; a <= 3; a++) e = c.cloneNode(0),
				g(e, {
					isShadow: "true",
					stroke: "rgb(0, 0, 0)",
					"stroke-opacity": 0.05 * a,
					"stroke-width": 7 - 2 * a,
					transform: "translate" + d,
					fill: Na
				}),
				c.parentNode.insertBefore(e, c),
				b.push(e);
				this.shadows = b
			}
			return this
		}
	};
	var Fb = function() {
		this.init.apply(this, arguments)
	};
	Fb.prototype = {
		init: function(a, b, e) {
			var c = location,
			d;
			this.Element = M;
			d = this.createElement("svg").attr({
				xmlns: "http://www.w3.org/2000/svg",
				version: "1.1"
			});
			a.appendChild(d.element);
			this.box = d.element;
			this.boxWrapper = d;
			this.alignedObjects = [];
			this.url = D ? "": c.href.replace(/#.*?$/, "");
			this.defs = this.createElement("defs").add();
			this.setSize(b, e, false)
		},
		createElement: function(a) {
			var b = new this.Element;
			b.init(this, a);
			return b
		},
		buildText: function(a) {
			for (var l = a.element, e = j(a.textStr, "").toString().replace(/<(b|strong)>/g, '<span style="font-weight:bold">').replace(/<(i|em)>/g, '<span style="font-style:italic">').replace(/<a/g, "<span").replace(/<\/(b|strong|i|em|a)>/g, "</span>").split(/<br[^>]?>/g), c = l.childNodes, d = /style="([^"]+)"/, f = /href="([^"]+)"/, h = g(l, "x"), n = (a = a.styles) && b(a.width), p = a && a.lineHeight, o, a = c.length; a--;) l.removeChild(c[a]);
			n && this.box.appendChild(l);
			y(e, function(a, i) {
				var e, c = 0,
				s, a = a.replace(/<span/g, "|||<span").replace(/<\/span>/g, "</span>|||");
				e = a.split("|||");
				y(e, function(a) {
					if (a !== "" || e.length == 1) {
						var j = {},
						q = A.createElementNS("http://www.w3.org/2000/svg", "tspan");
						d.test(a) && g(q, "style", a.match(d)[1].replace(/(;| |^)color([ :])/, "$1fill$2"));
						f.test(a) && (g(q, "onclick", 'location.href="' + a.match(f)[1] + '"'), m(q, {
							cursor: "pointer"
						}));
						a = a.replace(/<(.|\n)*?>/g, "") || " ";
						q.appendChild(A.createTextNode(a));
						c ? j.dx = 3: j.x = h;
						c || (i && (s = b(window.getComputedStyle(o, null).getPropertyValue("line-height")), isNaN(s) && (s = p || o.offsetHeight || 18), g(q, "dy", s)), o = q);
						g(q, j);
						l.appendChild(q);
						c++;
						if (n) for (var a = a.replace(/-/g, "- ").split(" "), t, R = []; a.length || R.length;) t = l.getBBox().width,
						j = t > n,
						! j || a.length == 1 ? (a = R, R = [], q = A.createElementNS("http://www.w3.org/2000/svg", "tspan"), g(q, {
							x: h,
							dy: p || 16
						}), l.appendChild(q), t > n && (n = t)) : (q.removeChild(q.firstChild), R.unshift(a.pop())),
						q.appendChild(A.createTextNode(a.join(" ").replace(/- /g, "-")))
					}
				})
			})
		},
		crispLine: function(a, b) {
			a[1] == a[4] && (a[1] = a[4] = x(a[1]) + b % 2 / 2);
			a[2] == a[5] && (a[2] = a[5] = x(a[2]) + b % 2 / 2);
			return a
		},
		path: function(a) {
			return this.createElement("path").attr({
				d: a,
				fill: Na
			})
		},
		circle: function(a, b, e) {
			a = d(a) ? a: {
				x: a,
				y: b,
				r: e
			};
			return this.createElement("circle").attr(a)
		},
		arc: function(a, b, e, c, g, j) {
			if (d(a)) b = a.y,
			e = a.r,
			c = a.innerR,
			g = a.start,
			j = a.end,
			a = a.x;
			return this.symbol("arc", a || 0, b || 0, e || 0, {
				innerR: c || 0,
				start: g || 0,
				end: j || 0
			})
		},
		rect: function(i, b, e, c, g, j) {
			if (arguments.length > 1) var f = (j || 0) % 2 / 2,
			i = x(i || 0) + f,
			b = x(b || 0) + f,
			e = x((e || 0) - 2 * f),
			c = x((c || 0) - 2 * f);
			f = d(i) ? i: {
				x: i,
				y: b,
				width: G(e, 0),
				height: G(c, 0)
			};
			return this.createElement("rect").attr(a(f, {
				rx: g || f.r,
				ry: g || f.r,
				fill: Na
			}))
		},
		setSize: function(a, b, e) {
			var c = this.alignedObjects,
			d = c.length;
			this.width = a;
			this.height = b;
			for (this.boxWrapper[j(e, true) ? "animate": "attr"]({
				width: a,
				height: b
			}); d--;) c[d].align()
		},
		g: function(a) {
			return this.createElement("g").attr(n(a) && {
				"class": db + a
			})
		},
		image: function(i, b, e, c, d) {
			var g = {
				preserveAspectRatio: Na
			};
			arguments.length > 1 && a(g, {
				x: b,
				y: e,
				width: c,
				height: d
			});
			g = this.createElement("image").attr(g);
			g.element.setAttributeNS("http://www.w3.org/1999/xlink", "href", i);
			return g
		},
		symbol: function(i, b, e, c, d) {
			var g, f = this.symbols[i],
			f = f && f(b, e, c, d),
			j = /^url\((.*?)\)$/;
			f ? (g = this.path(f), a(g, {
				symbolName: i,
				x: b,
				y: e,
				r: c
			}), d && a(g, d)) : j.test(i) ? (i = i.match(j)[1], g = this.image(i).attr({
				x: b,
				y: e
			}), t("img", {
				onload: function() {
					var a = Ja[this.src] || [this.width, this.height];
					g.attr({
						width: a[0],
						height: a[1]
					}).translate( - x(a[0] / 2), - x(a[1] / 2))
				},
				src: i
			})) : g = this.circle(b, e, c);
			return g
		},
		symbols: {
			square: function(a, b, e) {
				e *= 0.707;
				return [Ca, a - e, b - e, ma, a + e, b - e, a + e, b + e, a - e, b + e, "Z"]
			},
			triangle: function(a, b, e) {
				return [Ca, a, b - 1.33 * e, ma, a + e, b + 0.67 * e, a - e, b + 0.67 * e, "Z"]
			},
			"triangle-down": function(a, b, e) {
				return [Ca, a, b + 1.33 * e, ma, a - e, b - 0.67 * e, a + e, b - 0.67 * e, "Z"]
			},
			diamond: function(a, b, e) {
				return [Ca, a, b - e, ma, a + e, b, a, b + e, a - e, b, "Z"]
			},
			arc: function(a, b, e, c) {
				var d = c.start,
				g = c.end - 1.0E-6,
				f = c.innerR,
				j = Z(d),
				h = da(d),
				n = Z(g),
				g = da(g),
				c = c.end - d < P ? 0: 1;
				return [Ca, a + e * j, b + e * h, "A", e, e, 0, c, 1, a + e * n, b + e * g, ma, a + f * n, b + f * g, "A", f, f, 0, c, 0, a + f * j, b + f * h, "Z"]
			}
		},
		clipRect: function(a, b, e, c) {
			var d = db + Qa++,
			g = this.createElement("clipPath").attr({
				id: d
			}).add(this.defs),
			a = this.rect(a, b, e, c, 0).add(g);
			a.id = d;
			return a
		},
		color: function(a, b, e) {
			var c, d = /^rgba/;
			if (a && a.linearGradient) {
				var f = this,
				b = a.linearGradient,
				e = db + Qa++,
				j, h, n;
				j = f.createElement("linearGradient").attr({
					id: e,
					gradientUnits: "userSpaceOnUse",
					x1: b[0],
					y1: b[1],
					x2: b[2],
					y2: b[3]
				}).add(f.defs);
				y(a.stops, function(a) {
					d.test(a[1]) ? (c = La(a[1]), h = c.get("rgb"), n = c.get("a")) : (h = a[1], n = 1);
					f.createElement("stop").attr({
						offset: a[0],
						"stop-color": h,
						"stop-opacity": n
					}).add(j)
				});
				return "url(" + this.url + "#" + e + ")"
			} else return d.test(a) ? (c = La(a), g(b, e + "-opacity", c.get("a")), c.get("rgb")) : a
		},
		text: function(a, b, e) {
			var c = za.chart.style,
			b = x(j(b, 0)),
			e = x(j(e, 0)),
			a = this.createElement("text").attr({
				x: b,
				y: e,
				text: a
			}).css({
				"font-family": c.fontFamily,
				"font-size": c.fontSize
			});
			a.x = b;
			a.y = e;
			return a
		}
	};
	var W;
	if (!ca) {
		var sc = F(M, {
			init: function(a, b) {
				var e = ["<", b, ' filled="f" stroked="f"'],
				c = ["position: ", lb, ";"];
				(b == "shape" || b == $a) && c.push("left:0;top:0;width:10px;height:10px;");
				I && c.push("visibility: ", b == $a ? Ra: Ua);
				e.push(' style="', c.join(""), '"/>');
				if (b) e = b == $a || b == "span" || b == "img" ? e.join("") : a.prepVML(e),
				this.element = t(e);
				this.renderer = a
			},
			add: function(a) {
				var b = this.renderer,
				e = this.element,
				c = b.box,
				c = a ? a.element || a: c;
				a && a.inverted && b.invertChild(e, c);
				I && c.gVis == Ra && m(e, {
					visibility: Ra
				});
				c.appendChild(e);
				this.added = true;
				this.alignOnAdd && this.updateTransform();
				return this
			},
			attr: function(a, b) {
				var e, d, j, h = this.element || {},
				p = h.style,
				o = h.nodeName,
				q = this.renderer,
				z = this.symbolName,
				R, D, w = this.shadows,
				y = this;
				c(a) && n(b) && (e = a, a = {},
				a[e] = b);
				if (c(a)) e = a,
				y = e == "strokeWidth" || e == "stroke-width" ? this.strokeweight: this[e];
				else for (e in a) {
					d = a[e];
					R = false;
					if (z && /^(x|y|r|start|end|width|height|innerR)/.test(e)) D || (this.symbolAttr(a), D = true),
					R = true;
					else if (e == "d") {
						d = d || [];
						this.d = d.join(" ");
						j = d.length;
						for (R = []; j--;) R[j] = f(d[j]) ? x(d[j] * 10) - 5: d[j] == "Z" ? "x": d[j];
						d = R.join(" ") || "x";
						h.path = d;
						if (w) for (j = w.length; j--;) w[j].path = d;
						R = true
					} else if (e == "zIndex" || e == "visibility") {
						if (I && e == "visibility" && o == "DIV") {
							h.gVis = d;
							R = h.childNodes;
							for (j = R.length; j--;) m(R[j], {
								visibility: d
							});
							d == Ua && (d = null)
						}
						d && (p[e] = d);
						R = true
					} else if (/^(width|height)$/.test(e)) this.updateClipping ? (this[e] = d, this.updateClipping()) : p[e] = d,
					R = true;
					else if (/^(x|y)$/.test(e)) this[e] = d,
					h.tagName == "SPAN" ? this.updateTransform() : p[{
						x: "left",
						y: "top"
					} [e]] = d;
					else if (e == "class") h.className = d;
					else if (e == "stroke") d = q.color(d, h, e),
					e = "strokecolor";
					else if (e == "stroke-width" || e == "strokeWidth") h.stroked = d ? true: false,
					e = "strokeweight",
					this[e] = d,
					f(d) && (d += Ea);
					else if (e == "dashstyle")(h.getElementsByTagName("stroke")[0] || t(q.prepVML(["<stroke/>"]), null, null, h))[e] = d || "solid",
					this.dashstyle = d,
					R = true;
					else if (e == "fill") o == "SPAN" ? p.color = d: (h.filled = d != Na ? true: false, d = q.color(d, h, e), e = "fillcolor");
					else if (e == "translateX" || e == "translateY" || e == "rotation" || e == "align") e == "align" && (e = "textAlign"),
					this[e] = d,
					this.updateTransform(),
					R = true;
					else if (e == "text") h.innerHTML = d,
					R = true;
					if (w && e == "visibility") for (j = w.length; j--;) w[j].style[e] = d;
					R || (I ? h[e] = d: g(h, e, d))
				}
				return y
			},
			clip: function(a) {
				var b = this,
				e = a.members;
				e.push(b);
				b.destroyClip = function() {
					h(e, b)
				};
				return b.css(a.getCSS(b.inverted))
			},
			css: function(i) {
				var b = this.element;
				(b = i && i.width && b.tagName == "SPAN") && a(i, {
					display: "block",
					whiteSpace: "normal"
				});
				this.styles = a(this.styles, i);
				m(this.element, i);
				b && this.updateTransform();
				return this
			},
			destroy: function() {
				this.destroyClip && this.destroyClip();
				M.prototype.destroy.apply(this)
			},
			empty: function() {
				for (var a = this.element.childNodes, b = a.length, e; b--;) e = a[b],
				e.parentNode.removeChild(e)
			},
			getBBox: function() {
				var a = this.element;
				if (a.nodeName == "text") a.style.position = lb;
				return {
					x: a.offsetLeft,
					y: a.offsetTop,
					width: a.offsetWidth,
					height: a.offsetHeight
				}
			},
			on: function(a, b) {
				this.element["on" + a] = function() {
					var a = v.event;
					a.target = a.srcElement;
					b(a)
				};
				return this
			},
			updateTransform: function() {
				if (this.added) {
					var a = this,
					c = a.element,
					e = a.translateX || 0,
					d = a.translateY || 0,
					g = a.x || 0,
					j = a.y || 0,
					f = a.textAlign || "left",
					h = {
						left: 0,
						center: 0.5,
						right: 1
					} [f],
					p = f && f != "left";
					(e || d) && a.css({
						marginLeft: e,
						marginTop: d
					});
					a.inverted && y(c.childNodes, function(b) {
						a.renderer.invertChild(b, c)
					});
					if (c.tagName == "SPAN") {
						var o, q, e = a.rotation,
						t;
						o = 0;
						var d = 1,
						D = 0,
						w, I = a.xCorr || 0,
						v = a.yCorr || 0,
						B = [e, f, c.innerHTML, c.style.width].join(",");
						if (B != a.cTT) n(e) && (o = e * L, d = Z(o), D = da(o), m(c, {
							filter: e ? ["progid:DXImageTransform.Microsoft.Matrix(M11=", d, ", M12=", - D, ", M21=", D, ", M22=", d, ", sizingMethod='auto expand')"].join("") : Na
						})),
						o = c.offsetWidth,
						q = c.offsetHeight,
						t = x(b(c.style.fontSize || 12) * 1.2),
						I = d < 0 && - o,
						v = D < 0 && - q,
						w = d * D < 0,
						I += D * t * (w ? 1 - h: h),
						v -= d * t * (e ? w ? h: 1 - h: 1),
						p && (I -= o * h * (d < 0 ? - 1: 1), e && (v -= q * h * (D < 0 ? - 1: 1)), m(c, {
							textAlign: f
						})),
						a.xCorr = I,
						a.yCorr = v;
						m(c, {
							left: g + I,
							top: j + v
						});
						a.cTT = B
					}
				} else this.alignOnAdd = true
			},
			shadow: function(a) {
				var c = [],
				e = this.element,
				d = this.renderer,
				g,
				j = e.style,
				f,
				h = e.path;
				"" + e.path === "" && (h = "x");
				if (a) {
					for (a = 1; a <= 3; a++) f = ['<shape isShadow="true" strokeweight="', 7 - 2 * a, '" filled="false" path="', h, '" coordsize="100,100" style="', e.style.cssText, '" />'],
					g = t(d.prepVML(f), null, {
						left: b(j.left) + 1,
						top: b(j.top) + 1
					}),
					f = ['<stroke color="black" opacity="', 0.05 * a, '"/>'],
					t(d.prepVML(f), null, null, g),
					e.parentNode.insertBefore(g, e),
					c.push(g);
					this.shadows = c
				}
				return this
			}
		});
		W = function() {
			this.init.apply(this, arguments)
		};
		W.prototype = ia(Fb.prototype, {
			isIE8: U.indexOf("MSIE 8.0") > - 1,
			init: function(a, b, e) {
				var c;
				this.Element = sc;
				this.alignedObjects = [];
				c = this.createElement($a);
				a.appendChild(c.element);
				this.box = c.element;
				this.boxWrapper = c;
				this.setSize(b, e, false);
				if (!A.namespaces.hcv) A.namespaces.add("hcv", "urn:schemas-microsoft-com:vml"),
				A.createStyleSheet().cssText = "hcv\\:fill, hcv\\:path, hcv\\:shape, hcv\\:stroke{ behavior:url(#default#VML); display: inline-block; } "
			},
			clipRect: function(b, c, e, d) {
				var g = this.createElement();
				return a(g, {
					members: [],
					left: b,
					top: c,
					width: e,
					height: d,
					getCSS: function(b) {
						var e = this.top,
						i = this.left,
						c = i + this.width,
						l = e + this.height,
						e = {
							clip: "rect(" + x(b ? i: e) + "px," + x(b ? l: c) + "px," + x(b ? c: l) + "px," + x(b ? e: i) + "px)"
						}; ! b && I && a(e, {
							width: c + Ea,
							height: l + Ea
						});
						return e
					},
					updateClipping: function() {
						y(g.members, function(a) {
							a.css(g.getCSS(a.inverted))
						})
					}
				})
			},
			color: function(a, b, e) {
				var c, d = /^rgba/;
				if (a && a.linearGradient) {
					var g, j, f = a.linearGradient,
					h, n, p, o;
					y(a.stops, function(a, b) {
						d.test(a[1]) ? (c = La(a[1]), g = c.get("rgb"), j = c.get("a")) : (g = a[1], j = 1);
						b ? (p = g, o = j) : (h = g, n = j)
					});
					a = 90 - N.atan((f[3] - f[1]) / (f[2] - f[0])) * 180 / P;
					e = ["<", e, ' colors="0% ', h, ",100% ", p, '" angle="', a, '" opacity="', o, '" o:opacity2="', n, '" type="gradient" focus="100%" />'];
					t(this.prepVML(e), null, null, b)
				} else return d.test(a) && b.tagName != "IMG" ? (c = La(a), e = ["<", e, ' opacity="', c.get("a"), '"/>'], t(this.prepVML(e), null, null, b), c.get("rgb")) : a
			},
			prepVML: function(a) {
				var b = this.isIE8,
				a = a.join("");
				b ? (a = a.replace("/>", ' xmlns="urn:schemas-microsoft-com:vml" />'), a = a.indexOf('style="') == - 1 ? a.replace("/>", ' style="display:inline-block;behavior:url(#default#VML);" />') : a.replace('style="', 'style="display:inline-block;behavior:url(#default#VML);')) : a = a.replace("<", "<hcv:");
				return a
			},
			text: function(a, b, e) {
				var c = za.chart.style;
				return this.createElement("span").attr({
					text: a,
					x: x(b),
					y: x(e)
				}).css({
					whiteSpace: "nowrap",
					fontFamily: c.fontFamily,
					fontSize: c.fontSize
				})
			},
			path: function(a) {
				return this.createElement("shape").attr({
					coordsize: "100 100",
					d: a
				})
			},
			circle: function(a, b, e) {
				return this.path(this.symbols.circle(a, b, e))
			},
			g: function(a) {
				var b;
				a && (b = {
					className: db + a,
					"class": db + a
				});
				return this.createElement($a).attr(b)
			},
			image: function(a, b, e, c, d) {
				var g = this.createElement("img").attr({
					src: a
				});
				arguments.length > 1 && g.css({
					left: b,
					top: e,
					width: c,
					height: d
				});
				return g
			},
			rect: function(a, b, e, c, g, j) {
				if (arguments.length > 1) var f = (j || 0) % 2 / 2,
				a = x(a || 0) + f,
				b = x(b || 0) + f,
				e = x((e || 0) - 2 * f),
				c = x((c || 0) - 2 * f);
				if (d(a)) b = a.y,
				e = a.width,
				c = a.height,
				g = a.r,
				a = a.x;
				return this.symbol("rect", a || 0, b || 0, g || 0, {
					width: e || 0,
					height: c || 0
				})
			},
			invertChild: function(a, c) {
				var e = c.style;
				m(a, {
					flip: "x",
					left: b(e.width) - 10,
					top: b(e.height) - 10,
					rotation: - 90
				})
			},
			symbols: {
				arc: function(a, b, e, c) {
					var d = c.start,
					g = c.end,
					f = Z(d),
					j = da(d),
					h = Z(g),
					n = da(g),
					c = c.innerR;
					if (g - d === 0) return ["x"];
					else g - d == 2 * P && (h = - 0.07 / e);
					return ["wa", a - e, b - e, a + e, b + e, a + e * f, b + e * j, a + e * h, b + e * n, "at", a - c, b - c, a + c, b + c, a + c * h, b + c * n, a + c * f, b + c * j, "x", "e"]
				},
				circle: function(a, b, e) {
					return ["wa", a - e, b - e, a + e, b + e, a + e, b, a + e, b, "e"]
				},
				rect: function(a, b, e, c) {
					var d = c.width,
					c = c.height,
					g = a + d,
					f = b + c,
					e = Da(e, d, c);
					return [Ca, a + e, b, ma, g - e, b, "wa", g - 2 * e, b, g, b + 2 * e, g - e, b, g, b + e, ma, g, f - e, "wa", g - 2 * e, f - 2 * e, g, f, g, f - e, g - e, f, ma, a + e, f, "wa", a, f - 2 * e, a + 2 * e, f, a + e, f, a, f - e, ma, a, b + e, "wa", a, b, a + 2 * e, b + 2 * e, a, b + e, a + e, b, "x", "e"]
				}
			}
		})
	}
	var lc = ca ? Fb: W;
	Q.prototype.callbacks = [];
	var Ta = function() {};
	Ta.prototype = {
		init: function(a, b) {
			var e;
			this.series = a;
			this.applyOptions(b);
			this.pointAttr = {};
			if (a.options.colorByPoint) {
				e = a.chart.options.colors;
				if (!this.options) this.options = {};
				this.color = this.options.color = this.color || e[Ia++];
				Ia >= e.length && (Ia = 0)
			}
			a.chart.pointCount++;
			return this
		},
		applyOptions: function(b) {
			var l = this.series;
			this.config = b;
			if (f(b) || b === null) this.y = b;
			else if (d(b) && ! f(b.length)) a(this, b),
			this.options = b;
			else if (c(b[0])) this.name = b[0],
			this.y = b[1];
			else if (f(b[0])) this.x = b[0],
			this.y = b[1];
			if (this.x === ya) this.x = l.autoIncrement()
		},
		destroy: function() {
			var a = this,
			b = a.series,
			e;
			b.chart.pointCount--;
			a == b.chart.hoverPoint && a.onMouseOut();
			b.chart.hoverPoints = null;
			Va(a);
			y(["graphic", "tracker", "group", "dataLabel", "connector"], function(b) {
				a[b] && a[b].destroy()
			});
			a.legendItem && a.series.chart.legend.destroyItem(a);
			for (e in a) a[e] = null
		},
		select: function(a, b) {
			var e = this,
			c = e.series.chart;
			e.selected = a = j(a, ! e.selected);
			e.firePointEvent(a ? "select": "unselect");
			e.setState(a && "select");
			b || y(c.getSelectedPoints(), function(a) {
				if (a.selected && a != e) a.selected = false,
				a.setState(xa),
				a.firePointEvent("unselect")
			})
		},
		onMouseOver: function() {
			var a = this.series.chart,
			b = a.tooltip,
			e = a.hoverPoint;
			e && e != this && e.onMouseOut();
			this.firePointEvent("mouseOver");
			b && ! b.shared && b.refresh(this);
			this.setState(Sa);
			a.hoverPoint = this
		},
		onMouseOut: function() {
			this.firePointEvent("mouseOut");
			this.setState();
			this.series.chart.hoverPoint = null
		},
		tooltipFormatter: function(a) {
			var b = this.series;
			return ['<span style="color:' + b.color + '">', this.name || b.name, "</span>: ", ! a ? "<b>x = " + (this.name || this.x) + ",</b> ": "", "<b>", ! a ? "y = ": "", this.y, "</b><br/>"].join("")
		},
		update: function(a, b, e) {
			var c = this,
			d = c.series,
			g = d.chart;
			q(e, g);
			b = j(b, true);
			c.firePointEvent("update", {
				options: a
			},
			function() {
				c.applyOptions(a);
				d.isDirty = true;
				b && g.redraw()
			})
		},
		remove: function(a, b) {
			var e = this,
			c = e.series,
			d = c.chart,
			g = c.data;
			q(b, d);
			a = j(a, true);
			e.firePointEvent("remove", null, function() {
				h(g, e);
				e.destroy();
				c.isDirty = true;
				a && d.redraw()
			})
		},
		firePointEvent: function(a, b, e) {
			var c = this,
			d = this.series.options;
			(d.point.events[a] || c.options && c.options.events && c.options.events[a]) && this.importEvents();
			a == "click" && d.allowPointSelect && (e = function(a) {
				c.select(null, a.ctrlKey || a.metaKey || a.shiftKey)
			});
			ta(this, a, b, e)
		},
		importEvents: function() {
			if (!this.hasImportedEvents) {
				var a = ia(this.series.options.point, this.options).events,
				b;
				this.events = a;
				for (b in a) va(this, b, a[b]);
				this.hasImportedEvents = true
			}
		},
		setState: function(a) {
			var b = this.series,
			e = b.options.states,
			c = ka[b.type].marker && b.options.marker,
			d = c && ! c.enabled,
			g = (c = c && c.states[a]) && c.enabled === false,
			f = b.stateMarkerGraphic,
			j = b.chart,
			h = this.pointAttr;
			a || (a = xa);
			if (! (a == this.state || this.selected && a != "select" || e[a] && e[a].enabled === false || a && (g || d && ! c.enabled))) {
				if (this.graphic) this.graphic.attr(h[a]);
				else {
					if (a) {
						if (!f) b.stateMarkerGraphic = f = j.renderer.circle(0, 0, h[a].r).attr(h[a]).add(b.group);
						f.translate(this.plotX, this.plotY)
					}
					if (f) f[a ? "show": "hide"]()
				}
				this.state = a
			}
		}
	};
	var pa = function() {};
	pa.prototype = {
		isCartesian: true,
		type: "line",
		pointClass: Ta,
		pointAttrToOptions: {
			stroke: "lineColor",
			"stroke-width": "lineWidth",
			fill: "fillColor",
			r: "radius"
		},
		init: function(b, c) {
			var e, d;
			d = b.series.length;
			this.chart = b;
			c = this.setOptions(c);
			a(this, {
				index: d,
				options: c,
				name: c.name || "Series " + (d + 1),
				state: xa,
				pointAttr: {},
				visible: c.visible !== false,
				selected: c.selected === true
			});
			d = c.events;
			for (e in d) va(this, e, d[e]);
			if (d && d.click || c.point && c.point.events && c.point.events.click || c.allowPointSelect) b.runTrackerClick = true;
			this.getColor();
			this.getSymbol();
			this.setData(c.data, false)
		},
		autoIncrement: function() {
			var a = this.options,
			b = this.xIncrement,
			b = j(b, a.pointStart, 0);
			this.pointInterval = j(this.pointInterval, a.pointInterval, 1);
			this.xIncrement = b + this.pointInterval;
			return b
		},
		cleanData: function() {
			var a = this.chart,
			b = this.data,
			c, d, g = a.smallestInterval,
			f, j;
			b.sort(function(a, b) {
				return a.x - b.x
			});
			for (j = b.length - 1; j >= 0; j--) b[j - 1] && b[j - 1].x == b[j].x && b.splice(j - 1, 1);
			for (j = b.length - 1; j >= 0; j--) if (b[j - 1] && (f = b[j].x - b[j - 1].x, d === ya || f < d)) d = f,
			c = j;
			if (g === ya || d < g) a.smallestInterval = d;
			this.closestPoints = c
		},
		getSegments: function() {
			var a = - 1,
			b = [],
			c = this.data;
			y(c, function(d, g) {
				d.y === null ? (g > a + 1 && b.push(c.slice(a + 1, g)), a = g) : g == c.length - 1 && b.push(c.slice(a + 1, g + 1))
			});
			this.segments = b
		},
		setOptions: function(a) {
			var b = this.chart.options.plotOptions;
			return ia(b[this.type], b.series, a)
		},
		getColor: function() {
			var a = this.chart.options.colors;
			this.color = this.options.color || a[Ia++] || "#0000ff";
			Ia >= a.length && (Ia = 0)
		},
		getSymbol: function() {
			var a = this.chart.options.symbols;
			this.symbol = this.options.marker.symbol || a[Ya++];
			Ya >= a.length && (Ya = 0)
		},
		addPoint: function(a, b, c, d) {
			var g = this.data,
			f = this.graph,
			h = this.area,
			n = this.chart,
			a = (new this.pointClass).init(this, a);
			q(d, n);
			if (f && c) f.shift = c;
			if (h) h.shift = c,
			h.isArea = true;
			b = j(b, true);
			g.push(a);
			c && g[0].remove(false);
			this.isDirty = true;
			b && n.redraw()
		},
		setData: function(a, b) {
			var c = this,
			d = c.data,
			g = c.initialColor,
			f = c.chart,
			h = d && d.length || 0;
			c.xIncrement = null;
			n(g) && (Ia = g);
			for (a = kb(p(a || []), function(a) {
				return (new c.pointClass).init(c, a)
			}); h--;) d[h].destroy();
			c.data = a;
			c.cleanData();
			c.getSegments();
			c.isDirty = true;
			f.isDirtyBox = true;
			j(b, true) && f.redraw(false)
		},
		remove: function(a, b) {
			var c = this,
			d = c.chart,
			a = j(a, true);
			if (!c.isRemoving) c.isRemoving = true,
			ta(c, "remove", null, function() {
				c.destroy();
				d.isDirtyLegend = d.isDirtyBox = true;
				a && d.redraw(b)
			});
			c.isRemoving = false
		},
		translate: function() {
			for (var a = this.chart, b = this.options.stacking, c = this.xAxis.categories, d = this.yAxis, g = this.data, f = g.length; f--;) {
				var j = g[f],
				h = j.x,
				p = j.y,
				o = j.low,
				m = d.stacks[(p < 0 ? "-": "") + this.stackKey];
				j.plotX = this.xAxis.translate(h);
				if (b && this.visible && m[h]) o = m[h],
				h = o.total,
				o.cum = o = o.cum - p,
				p = o + p,
				b == "percent" && (o = h ? o * 100 / h: 0, p = h ? p * 100 / h: 0),
				j.percentage = h ? j.y * 100 / h: 0,
				j.stackTotal = h;
				if (n(o)) j.yBottom = d.translate(o, 0, 1);
				if (p !== null) j.plotY = d.translate(p, 0, 1);
				j.clientX = a.inverted ? a.plotHeight - j.plotX: j.plotX;
				j.category = c && c[j.x] !== ya ? c[j.x] : j.x
			}
		},
		setTooltipPoints: function(a) {
			var b = this.chart,
			c = b.inverted,
			d = [],
			g = x((c ? b.plotTop: b.plotLeft) + b.plotSizeX),
			j,
			f,
			h = [];
			if (a) this.tooltipPoints = null;
			y(this.segments, function(a) {
				d = d.concat(a)
			});
			this.xAxis && this.xAxis.reversed && (d = d.reverse());
			y(d, function(a, b) {
				j = d[b - 1] ? d[b - 1].high + 1: 0;
				for (f = a.high = d[b + 1] ? ha((a.plotX + (d[b + 1] ? d[b + 1].plotX: g)) / 2) : g; j <= f;) h[c ? g - j++ : j++] = a
			});
			this.tooltipPoints = h
		},
		onMouseOver: function() {
			var a = this.chart,
			b = a.hoverSeries;
			if (Ha || ! a.mouseIsDown) b && b != this && b.onMouseOut(),
			this.options.events.mouseOver && ta(this, "mouseOver"),
			this.tracker && this.tracker.toFront(),
			this.setState(Sa),
			a.hoverSeries = this
		},
		onMouseOut: function() {
			var a = this.options,
			b = this.chart,
			c = b.tooltip,
			d = b.hoverPoint;
			d && d.onMouseOut();
			this && a.events.mouseOut && ta(this, "mouseOut");
			c && ! a.stickyTracking && c.hide();
			this.setState();
			b.hoverSeries = null
		},
		animate: function(a) {
			var b = this.chart,
			c = this.clipRect,
			g = this.options.animation;
			g && ! d(g) && (g = {});
			if (a) {
				if (!c.isAnimating) c.attr("width", 0),
				c.isAnimating = true
			} else c.animate({
				width: b.plotSizeX
			},
			g),
			this.animate = null
		},
		drawPoints: function() {
			var a, b = this.data,
			c = this.chart,
			d, g, f, h, n, p;
			if (this.options.marker.enabled) for (f = b.length; f--;) if (h = b[f], d = h.plotX, g = h.plotY, p = h.graphic, g !== ya && ! isNaN(g)) a = h.pointAttr[h.selected ? "select": xa],
			n = a.r,
			p ? p.animate({
				x: d,
				y: g,
				r: n
			}) : h.graphic = c.renderer.symbol(j(h.marker && h.marker.symbol, this.symbol), d, g, n).attr(a).add(this.group)
		},
		convertAttribs: function(a, b, c, d) {
			var g = this.pointAttrToOptions,
			f, h, n = {},
			a = a || {},
			b = b || {},
			c = c || {},
			d = d || {};
			for (f in g) h = g[f],
			n[f] = j(a[h], b[f], c[f], d[f]);
			return n
		},
		getAttribs: function() {
			var a = this,
			b = ka[a.type].marker ? a.options.marker: a.options,
			c = b.states,
			d = c[Sa],
			g,
			f = a.color,
			j = {
				stroke: f,
				fill: f
			},
			h = a.data,
			p = [],
			o,
			m = a.pointAttrToOptions;
			a.options.marker ? (d.radius = d.radius || b.radius + 2, d.lineWidth = d.lineWidth || b.lineWidth + 1) : d.color = d.color || La(d.color || f).brighten(d.brightness).get();
			p[xa] = a.convertAttribs(b, j);
			y([Sa, "select"], function(b) {
				p[b] = a.convertAttribs(c[b], p[xa])
			});
			a.pointAttr = p;
			for (f = h.length; f--;) {
				j = h[f];
				if ((b = j.options && j.options.marker || j.options) && b.enabled === false) b.radius = 0;
				g = false;
				if (j.options) for (var q in m) n(b[m[q]]) && (g = true);
				if (g) {
					o = [];
					c = b.states || {};
					g = c[Sa] = c[Sa] || {};
					if (!a.options.marker) g.color = La(g.color || j.options.color).brighten(g.brightness || d.brightness).get();
					o[xa] = a.convertAttribs(b, p[xa]);
					o[Sa] = a.convertAttribs(c[Sa], p[Sa], o[xa]);
					o.select = a.convertAttribs(c.select, p.select, o[xa])
				} else o = p;
				j.pointAttr = o
			}
		},
		destroy: function() {
			var a = this,
			b = a.chart,
			c = /\/5[0-9\.]+ Safari\//.test(U),
			d,
			g;
			Va(a);
			a.legendItem && a.chart.legend.destroyItem(a);
			y(a.data, function(a) {
				a.destroy()
			});
			y(["area", "graph", "dataLabelsGroup", "group", "tracker"], function(b) {
				a[b] && (d = c && b == "group" ? "hide": "destroy", a[b][d]())
			});
			if (b.hoverSeries == a) b.hoverSeries = null;
			h(b.series, a);
			for (g in a) delete a[g]
		},
		drawDataLabels: function() {
			if (this.options.dataLabels.enabled) {
				var a = this,
				b, c, d = a.data,
				g = a.options.dataLabels,
				f, h = a.dataLabelsGroup,
				n = a.chart,
				p = n.inverted,
				o = a.type,
				m;
				if (!h) h = a.dataLabelsGroup = n.renderer.g(db + "data-labels").attr({
					visibility: a.visible ? Ua: Ra,
					zIndex: 5
				}).translate(n.plotLeft, n.plotTop).add();
				m = g.color;
				m == "auto" && (m = null);
				g.style.color = j(m, a.color);
				y(d, function(d) {
					var m = d.barX,
					m = m && m + d.barW / 2 || d.plotX || - 999,
					s = j(d.plotY, - 999),
					q = d.dataLabel,
					t = g.align;
					f = g.formatter.call({
						x: d.x,
						y: d.y,
						series: a,
						point: d,
						percentage: d.percentage,
						total: d.total || d.stackTotal
					});
					b = (p ? n.plotWidth - s: m) + g.x;
					c = (p ? n.plotHeight - m: s) + g.y;
					o == "column" && (b += {
						left: - 1,
						right: 1
					} [t] * d.barW / 2 || 0);
					if (q) q.animate({
						x: b,
						y: c
					});
					else if (f) q = d.dataLabel = n.renderer.text(f, b, c).attr({
						align: t,
						rotation: g.rotation,
						zIndex: 1
					}).css(g.style).add(h);
					p && ! g.y && q.attr({
						y: c + parseInt(q.styles.lineHeight) * 0.9 - q.getBBox().height / 2
					})
				})
			}
		},
		drawGraph: function() {
			var a = this,
			b = a.options,
			c = a.graph,
			d = [],
			g,
			f = a.area,
			h = a.group,
			n = b.lineColor || a.color,
			p = b.lineWidth,
			o = b.dashStyle,
			m,
			q = a.chart.renderer,
			t = a.yAxis.getThreshold(b.threshold || 0),
			D = /^area/.test(a.type),
			w = [],
			I = [];
			y(a.segments, function(c) {
				m = [];
				y(c, function(e, d) {
					a.getPointSpline ? m.push.apply(m, a.getPointSpline(c, e, d)) : (m.push(d ? ma: Ca), d && b.step && m.push(e.plotX, c[d - 1].plotY), m.push(e.plotX, e.plotY))
				});
				c.length > 1 ? d = d.concat(m) : w.push(c[0]);
				if (D) {
					var e = [],
					g,
					f = m.length;
					for (g = 0; g < f; g++) e.push(m[g]);
					f == 3 && e.push(ma, m[1], m[2]);
					if (b.stacking && a.type != "areaspline") for (g = c.length - 1; g >= 0; g--) e.push(c[g].plotX, c[g].yBottom);
					else e.push(ma, c[c.length - 1].plotX, t, ma, c[0].plotX, t);
					I = I.concat(e)
				}
			});
			a.graphPath = d;
			a.singlePoints = w;
			if (D) g = j(b.fillColor, La(a.color).setOpacity(b.fillOpacity || 0.75).get()),
			f ? f.animate({
				d: I
			}) : a.area = a.chart.renderer.path(I).attr({
				fill: g
			}).add(h);
			if (c) c.animate({
				d: d
			});
			else if (p) {
				c = {
					stroke: n,
					"stroke-width": p
				};
				if (o) c.dashstyle = o;
				a.graph = q.path(d).attr(c).add(h).shadow(b.shadow)
			}
		},
		render: function() {
			var a = this,
			b = a.chart,
			c, d, g = a.options,
			f = g.animation,
			j = f && a.animate,
			f = j ? f && f.duration || 500: 0,
			h = a.clipRect;
			d = b.renderer;
			if (!h && (h = a.clipRect = ! b.hasRendered && b.clipRect ? b.clipRect: d.clipRect(0, 0, b.plotSizeX, b.plotSizeY), ! b.clipRect)) b.clipRect = h;
			if (!a.group) c = a.group = d.g("series"),
			b.inverted && (d = function() {
				c.attr({
					width: b.plotWidth,
					height: b.plotHeight
				}).invert()
			},
			d(), va(b, "resize", d)),
			c.clip(a.clipRect).attr({
				visibility: a.visible ? Ua: Ra,
				zIndex: g.zIndex
			}).translate(b.plotLeft, b.plotTop).add(b.seriesGroup);
			a.drawDataLabels();
			j && a.animate(true);
			a.getAttribs();
			a.drawGraph && a.drawGraph();
			a.drawPoints();
			a.options.enableMouseTracking !== false && a.drawTracker();
			j && a.animate();
			setTimeout(function() {
				h.isAnimating = false;
				if ((c = a.group) && h != b.clipRect && h.renderer) c.clip(a.clipRect = b.clipRect),
				h.destroy()
			},
			f);
			a.isDirty = false
		},
		redraw: function() {
			var a = this.chart,
			b = this.group;
			b && (a.inverted && b.attr({
				width: a.plotWidth,
				height: a.plotHeight
			}), b.animate({
				translateX: a.plotLeft,
				translateY: a.plotTop
			}));
			this.translate();
			this.setTooltipPoints(true);
			this.render()
		},
		setState: function(a) {
			var b = this.options,
			c = this.graph,
			d = b.states,
			b = b.lineWidth,
			a = a || xa;
			if (this.state != a) this.state = a,
			d[a] && d[a].enabled === false || (a && (b = d[a].lineWidth || b + 1), c && ! c.dashstyle && c.attr({
				"stroke-width": b
			},
			a ? 0: 500))
		},
		setVisible: function(a, b) {
			var c = this.chart,
			d = this.legendItem,
			g = this.group,
			f = this.tracker,
			j = this.dataLabelsGroup,
			h, n = this.data,
			p = c.options.chart.ignoreHiddenSeries;
			h = this.visible;
			h = (this.visible = a = a === ya ? ! h: a) ? "show": "hide";
			g && g[h]();
			if (f) f[h]();
			else for (g = n.length; g--;) f = n[g],
			f.tracker && f.tracker[h]();
			j && j[h]();
			d && c.legend.colorizeItem(this, a);
			this.isDirty = true;
			this.options.stacking && y(c.series, function(a) {
				if (a.options.stacking && a.visible) a.isDirty = true
			});
			if (p) c.isDirtyBox = true;
			b !== false && c.redraw();
			ta(this, h)
		},
		show: function() {
			this.setVisible(true)
		},
		hide: function() {
			this.setVisible(false)
		},
		select: function(a) {
			this.selected = a = a === ya ? ! this.selected: a;
			if (this.checkbox) this.checkbox.checked = a;
			ta(this, a ? "select": "unselect")
		},
		drawTracker: function() {
			var a = this,
			b = a.options,
			c = [].concat(a.graphPath),
			d = c.length,
			g = a.chart,
			f = g.options.tooltip.snap,
			j = a.tracker,
			h = b.cursor,
			h = h && {
				cursor: h
			},
			n = a.singlePoints,
			p;
			if (d) for (p = d + 1; p--;) c[p] == Ca && c.splice(p + 1, 0, c[p + 1] - f, c[p + 2], ma),
			(p && c[p] == Ca || p == d) && c.splice(p, 0, ma, c[p - 2] + f, c[p - 1]);
			for (p = 0; p < n.length; p++) d = n[p],
			c.push(Ca, d.plotX - f, d.plotY, ma, d.plotX + f, d.plotY);
			j ? j.attr({
				d: c
			}) : a.tracker = g.renderer.path(c).attr({
				isTracker: true,
				stroke: tb,
				fill: Na,
				"stroke-width": b.lineWidth + 2 * f,
				visibility: a.visible ? Ua: Ra,
				zIndex: 1
			}).on(Ha ? "touchstart": "mouseover", function() {
				g.hoverSeries != a && a.onMouseOver()
			}).on("mouseout", function() {
				b.stickyTracking || a.onMouseOut()
			}).css(h).add(g.trackerGroup)
		}
	};
	W = F(pa);
	Pa.line = W;
	W = F(pa, {
		type: "area"
	});
	Pa.area = W;
	W = F(pa, {
		type: "spline",
		getPointSpline: function(a, b, c) {
			var d = b.plotX,
			g = b.plotY,
			f = a[c - 1],
			j = a[c + 1],
			h,
			p,
			n,
			o;
			if (c && c < a.length - 1) {
				a = f.plotY;
				n = j.plotX;
				var j = j.plotY,
				m;
				h = (1.5 * d + f.plotX) / 2.5;
				p = (1.5 * g + a) / 2.5;
				n = (1.5 * d + n) / 2.5;
				o = (1.5 * g + j) / 2.5;
				m = (o - p) * (n - d) / (n - h) + g - o;
				p += m;
				o += m;
				p > a && p > g ? (p = G(a, g), o = 2 * g - p) : p < a && p < g && (p = Da(a, g), o = 2 * g - p);
				o > j && o > g ? (o = G(j, g), p = 2 * g - o) : o < j && o < g && (o = Da(j, g), p = 2 * g - o);
				b.rightContX = n;
				b.rightContY = o
			}
			c ? (b = ["C", f.rightContX || f.plotX, f.rightContY || f.plotY, h || d, p || g, d, g], f.rightContX = f.rightContY = null) : b = [Ca, d, g];
			return b
		}
	});
	Pa.spline = W;
	W = F(W, {
		type: "areaspline"
	});
	Pa.areaspline = W;
	var Za = F(pa, {
		type: "column",
		pointAttrToOptions: {
			stroke: "borderColor",
			"stroke-width": "borderWidth",
			fill: "color",
			r: "borderRadius"
		},
		init: function() {
			pa.prototype.init.apply(this, arguments);
			var a = this,
			b = a.chart;
			b.hasColumn = true;
			b.hasRendered && y(b.series, function(b) {
				if (b.type == a.type) b.isDirty = true
			})
		},
		translate: function() {
			var b = this,
			c = b.chart,
			d = 0,
			g = b.xAxis.reversed,
			f = b.xAxis.categories,
			h = {},
			p, o;
			pa.prototype.translate.apply(b);
			y(c.series, function(a) {
				if (a.type == b.type) a.options.stacking ? (p = a.stackKey, h[p] === ya && (h[p] = d++), o = h[p]) : o = d++,
				a.columnIndex = o
			});
			var m = b.options,
			q = b.data,
			t = b.closestPoints,
			c = Y(q[1] ? q[t].plotX - q[t - 1].plotX: c.plotSizeX / (f ? f.length: 1)),
			f = c * m.groupPadding,
			t = (c - 2 * f) / d,
			D = m.pointWidth,
			I = n(D) ? (t - D) / 2: t * m.pointPadding,
			w = j(D, t - 2 * I),
			x = I + (f + ((g ? d - b.columnIndex: b.columnIndex) || 0) * t - c / 2) * (g ? - 1: 1),
			v = b.yAxis.getThreshold(m.threshold || 0),
			B = j(m.minPointLength, 5);
			y(q, function(b) {
				var c = b.plotY,
				d = b.yBottom || v,
				e = b.plotX + x,
				g = gb(Da(c, d)),
				f = gb(G(c, d) - g),
				j;
				Y(f) < B && (B && (f = B, g = Y(g - v) > B ? d - B: v - (c <= v ? B: 0)), j = g - 3);
				a(b, {
					barX: e,
					barY: g,
					barW: w,
					barH: f
				});
				b.shapeType = "rect";
				b.shapeArgs = {
					x: e,
					y: g,
					width: w,
					height: f,
					r: m.borderRadius
				};
				b.trackerArgs = n(j) && ia(b.shapeArgs, {
					height: G(6, f + 3),
					y: j
				})
			})
		},
		getSymbol: function() {},
		drawGraph: function() {},
		drawPoints: function() {
			var a = this,
			b = a.options,
			c = a.chart.renderer,
			d, g;
			y(a.data, function(f) {
				var j = f.plotY;
				if (j !== ya && ! isNaN(j)) d = f.graphic,
				g = f.shapeArgs,
				d ? (Eb(d), d.animate(g)) : f.graphic = c[f.shapeType](g).attr(f.pointAttr[f.selected ? "select": xa]).add(a.group).shadow(b.shadow)
			})
		},
		drawTracker: function() {
			var a = this,
			b = a.chart,
			c = b.renderer,
			d, f, j = + new Date,
			h = a.options.cursor,
			p = h && {
				cursor: h
			},
			n;
			y(a.data, function(h) {
				f = h.tracker;
				d = h.trackerArgs || h.shapeArgs;
				if (h.y !== null) f ? f.attr(d) : h.tracker = c[h.shapeType](d).attr({
					isTracker: j,
					fill: tb,
					visibility: a.visible ? Ua: Ra,
					zIndex: 1
				}).on(Ha ? "touchstart": "mouseover", function(c) {
					n = c.relatedTarget || c.fromElement;
					b.hoverSeries != a && g(n, "isTracker") != j && a.onMouseOver();
					h.onMouseOver()
				}).on("mouseout", function(b) {
					a.options.stickyTracking || (n = b.relatedTarget || b.toElement, g(n, "isTracker") != j && a.onMouseOut())
				}).css(p).add(b.trackerGroup)
			})
		},
		animate: function(a) {
			var b = this,
			c = b.data;
			if (!a) y(c, function(a) {
				var c = a.graphic;
				c && (c.attr({
					height: 0,
					y: b.yAxis.translate(0, 0, 1)
				}), c.animate({
					height: a.barH,
					y: a.barY
				},
				b.options.animation))
			}),
			b.animate = null
		},
		remove: function() {
			var a = this,
			b = a.chart;
			b.hasRendered && y(b.series, function(b) {
				if (b.type == a.type) b.isDirty = true
			});
			pa.prototype.remove.apply(a, arguments)
		}
	});
	Pa.column = Za;
	W = F(Za, {
		type: "bar",
		init: function(a) {
			a.inverted = this.inverted = true;
			Za.prototype.init.apply(this, arguments)
		}
	});
	Pa.bar = W;
	W = F(pa, {
		type: "scatter",
		translate: function() {
			var a = this;
			pa.prototype.translate.apply(a);
			y(a.data, function(b) {
				b.shapeType = "circle";
				b.shapeArgs = {
					x: b.plotX,
					y: b.plotY,
					r: a.chart.options.tooltip.snap
				}
			})
		},
		drawTracker: function() {
			var a = this,
			b = a.options.cursor,
			c = b && {
				cursor: b
			},
			d;
			y(a.data, function(b) { (d = b.graphic) && d.attr({
					isTracker: true
				}).on("mouseover", function() {
					a.onMouseOver();
					b.onMouseOver()
				}).on("mouseout", function() {
					a.options.stickyTracking || a.onMouseOut()
				}).css(c)
			})
		},
		cleanData: function() {}
	});
	Pa.scatter = W;
	W = F(Ta, {
		init: function() {
			Ta.prototype.init.apply(this, arguments);
			var b = this,
			c;
			a(b, {
				visible: b.visible !== false,
				name: j(b.name, "Slice")
			});
			c = function() {
				b.slice()
			};
			va(b, "select", c);
			va(b, "unselect", c);
			return b
		},
		setVisible: function(a) {
			var b = this.series.chart,
			c = this.tracker,
			d = this.dataLabel,
			g = this.connector,
			f;
			f = (this.visible = a = a === ya ? ! this.visible: a) ? "show": "hide";
			this.group[f]();
			c && c[f]();
			d && d[f]();
			g && g[f]();
			this.legendItem && b.legend.colorizeItem(this, a)
		},
		slice: function(a, b, c) {
			var d = this.series.chart,
			g = this.slicedTranslation;
			q(c, d);
			j(b, true);
			a = this.sliced = n(a) ? a: ! this.sliced;
			this.group.animate({
				translateX: a ? g[0] : d.plotLeft,
				translateY: a ? g[1] : d.plotTop
			})
		}
	});
	W = F(pa, {
		type: "pie",
		isCartesian: false,
		pointClass: W,
		pointAttrToOptions: {
			stroke: "borderColor",
			"stroke-width": "borderWidth",
			fill: "color"
		},
		getColor: function() {
			this.initialColor = Ia
		},
		animate: function() {
			var a = this;
			y(a.data, function(b) {
				var c = b.graphic,
				b = b.shapeArgs,
				d = - P / 2;
				c && (c.attr({
					r: 0,
					start: d,
					end: d
				}), c.animate({
					r: b.r,
					start: b.start,
					end: b.end
				},
				a.options.animation))
			});
			a.animate = null
		},
		translate: function() {
			var a = 0,
			c = - 0.25,
			d = this.options,
			g = d.slicedOffset,
			f = g + d.borderWidth,
			j = d.center,
			h = this.chart,
			p = h.plotWidth,
			n = h.plotHeight,
			o, m, q, t = this.data,
			D = 2 * P,
			I, w = Da(p, n),
			v,
			ca,
			Ba = d.dataLabels.distance;
			j.push(d.size, d.innerSize || 0);
			j = kb(j, function(a, c) {
				return /%$/.test(a) ? [p, n, w, w][c] * b(a) / 100: a
			});
			this.getX = function(a, b) {
				q = N.asin((a - j[1]) / (j[2] / 2 + Ba));
				return j[0] + (b ? - 1: 1) * Z(q) * (j[2] / 2 + Ba)
			};
			this.center = j;
			y(t, function(b) {
				a += b.y
			});
			y(t, function(b) {
				I = a ? b.y / a: 0;
				o = x(c * D * 1E3) / 1E3;
				c += I;
				m = x(c * D * 1E3) / 1E3;
				b.shapeType = "arc";
				b.shapeArgs = {
					x: j[0],
					y: j[1],
					r: j[2] / 2,
					innerR: j[3] / 2,
					start: o,
					end: m
				};
				q = (m + o) / 2;
				b.slicedTranslation = kb([Z(q) * g + h.plotLeft, da(q) * g + h.plotTop], x);
				v = Z(q) * j[2] / 2;
				ca = da(q) * j[2] / 2;
				b.tooltipPos = [j[0] + v * 0.7, j[1] + ca * 0.7];
				b.labelPos = [j[0] + v + Z(q) * Ba, j[1] + ca + da(q) * Ba, j[0] + v + Z(q) * f, j[1] + ca + da(q) * f, j[0] + v, j[1] + ca, Ba < 0 ? "center": q < D / 4 ? "left": "right", q];
				b.percentage = I * 100;
				b.total = a
			});
			this.setTooltipPoints()
		},
		render: function() {
			this.getAttribs();
			this.drawPoints();
			this.options.enableMouseTracking !== false && this.drawTracker();
			this.drawDataLabels();
			this.options.animation && this.animate && this.animate();
			this.isDirty = false
		},
		drawPoints: function() {
			var b = this.chart,
			c = b.renderer,
			d, g, f, j;
			y(this.data, function(h) {
				g = h.graphic;
				j = h.shapeArgs;
				f = h.group;
				if (!f) f = h.group = c.g("point").attr({
					zIndex: 5
				}).add();
				d = h.sliced ? h.slicedTranslation: [b.plotLeft, b.plotTop];
				f.translate(d[0], d[1]);
				g ? g.animate(j) : h.graphic = c.arc(j).attr(a(h.pointAttr[xa], {
					"stroke-linejoin": "round"
				})).add(h.group);
				h.visible === false && h.setVisible(false)
			})
		},
		drawDataLabels: function() {
			var a = this.data,
			b, c = this.chart,
			d = this.options.dataLabels,
			g = j(d.connectorPadding, 10),
			f = j(d.connectorWidth, 1),
			h,
			p,
			n = d.distance > 0,
			o,
			m,
			q = this.center[1],
			t = [[], [], [], []],
			D,
			I,
			w,
			v,
			x,
			ca,
			Ba,
			F = 4,
			A;
			pa.prototype.drawDataLabels.apply(this);
			y(a, function(a) {
				var b = a.labelPos[7];
				t[b < 0 ? 0: b < P / 2 ? 1: b < P ? 2: 3].push(a)
			});
			t[1].reverse();
			t[3].reverse();
			for (Ba = function(a, b) {
				return a.y > b.y
			}; F--;) {
				a = 0;
				b = [].concat(t[F]);
				b.sort(Ba);
				for (A = b.length; A--;) b[A].rank = A;
				for (v = 0; v < 2; v++) {
					m = (ca = F % 3) ? 9999: - 9999;
					x = ca ? - 1: 1;
					for (A = 0; A < t[F].length; A++) if (b = t[F][A], h = b.dataLabel) {
						p = b.labelPos;
						w = Ua;
						D = p[0];
						I = p[1];
						o || (o = h && h.getBBox().height);
						if (n) if (v && b.rank < a) w = Ra;
						else if (!ca && I < m + o || ca && I > m - o) if (I = m + x * o, D = this.getX(I, F > 1), ! ca && I + o > q || ca && I - o < q) v ? w = Ra: a++;
						b.visible === false && (w = Ra);
						w == Ua && (m = I);
						if (v && (h.attr({
							visibility: w,
							align: p[6]
						})[h.moved ? "animate": "attr"]({
							x: D + d.x + ({
								left: g,
								right: - g
							} [p[6]] || 0),
							y: I + d.y
						}), h.moved = true, n && f)) h = b.connector,
						p = [Ca, D + (p[6] == "left" ? 5: - 5), I, ma, D, I, ma, p[2], p[3], ma, p[4], p[5]],
						h ? (h.animate({
							d: p
						}), h.attr("visibility", w)) : b.connector = h = this.chart.renderer.path(p).attr({
							"stroke-width": f,
							stroke: d.connectorColor || "#606060",
							visibility: w,
							zIndex: 3
						}).translate(c.plotLeft, c.plotTop).add()
					}
				}
			}
		},
		drawTracker: Za.prototype.drawTracker,
		getSymbol: function() {}
	});
	Pa.pie = W;
	v.Highcharts = {
		Chart: Q,
		dateFormat: Ab,
		pathAnim: cb,
		getOptions: function() {
			return za
		},
		numberFormat: Ma,
		Point: Ta,
		Color: La,
		Renderer: lc,
		seriesTypes: Pa,
		setOptions: function(a) {
			za = ia(za, a);
			w();
			return za
		},
		Series: pa,
		addEvent: va,
		createElement: t,
		discardElement: aa,
		css: m,
		each: y,
		extend: a,
		map: kb,
		merge: ia,
		pick: j,
		extendClass: F,
		version: "2.1.2"
	}
})();
var treeio = {
	put_mce: function(a) { (a ? $("textarea", a) : $("textarea")).each(function() {
			$(this).hasClass("no-editor") || ($(this).attr("id", a.attr("id") + "-" + $(this).attr("id")), $(this).hasClass("full-editor") ? $(this).tinymce({
				script_url: "/static/js/tinymce/jscripts/tiny_mce/tiny_mce.js",
				theme: "advanced",
				skin: "cirkuit",
				relative_urls: false,
				plugins: "safari,table,advhr,inlinepopups,insertdatetime,preview,searchreplace,contextmenu,paste,fullscreen,nonbreaking,visualchars,xhtmlxtras",
				theme_advanced_buttons1: "bold,italic,underline,strikethrough,|,justifyleft,justifycenter,justifyright,justifyfull,formatselect,fontselect,fontsizeselect,|,cut,copy,paste,pastetext,pasteword,|,search,replace",
				theme_advanced_buttons2: "bullist,numlist,|,outdent,indent,blockquote,|,undo,redo,|,link,unlink,image,cleanup,code,|,insertdate,inserttime,preview,|,forecolor,backcolor,|,cite,abbr,acronym,del,ins",
				theme_advanced_buttons3: "tablecontrols,|,hr,removeformat,|,sub,sup,|,visualchars,nonbreaking,charmap,advhr,|,fullscreen",
				theme_advanced_disable: "help,styleselect,anchor,newdocument",
				theme_advanced_toolbar_location: "top",
				theme_advanced_toolbar_align: "left",
				theme_advanced_statusbar_location: "bottom",
				theme_advanced_resizing: true,
				theme_advanced_resize_horizontal: true,
				theme_advanced_resizing_use_cookie: true,
				theme_advanced_path: false,
				width: "70%"
			}) : $(this).tinymce({
				script_url: "/static/js/tinymce/jscripts/tiny_mce/tiny_mce.js",
				theme: "advanced",
				skin: "cirkuit",
				relative_urls: false,
				plugins: "safari,table,advhr,inlinepopups,insertdatetime,preview,searchreplace,contextmenu,paste,fullscreen,nonbreaking,visualchars,xhtmlxtras",
				theme_advanced_statusbar_location: "bottom",
				theme_advanced_toolbar_location: "top",
				theme_advanced_toolbar_align: "left",
				theme_advanced_path: false,
				theme_advanced_resizing: true,
				theme_advanced_resize_horizontal: true,
				theme_advanced_resizing_use_cookie: true,
				theme_advanced_disable: "justifyleft,justifycenter,justifyright,justifyfull,outdent,indent,image,help,hr,removeformat,formatselect,fontselect,fontsizeselect,styleselect,sub,sup,forecolor,backcolor,forecolorpicker,backcolorpicker,charmap,visualaid,anchor,newdocument,blockquote",
				theme_advanced_buttons1: "bold,italic,underline,strikethrough,|,undo,redo,|,cut,copy,paste,link,unlink,cleanup,|,bullist,numlist,|,code",
				theme_advanced_buttons2: "",
				theme_advanced_buttons3: "",
				width: "70%"
			}))
		})
	},
	remove_mce: function(a) { (a ? $("textarea", a) : $("textarea")).each(function() {
			tinyMCE.execCommand("mceRemoveControl", false, $(this).attr("id"))
		})
	},
	do_ajax: function() {
		var a = window.location.hash.replace(/#/gi, "");
		if (!a) a = window.location.pathname;
		var b = $('.menu-item a[href="#' + a + '"]');
		if (b.length && ! b.hasClass("active") && (block = $("#module-" + b.attr("id").substring(5)), block.length)) $(".module-block").each(function() {
			$(this).attr("id") != block.attr("id") ? ($(this).css("display", "none"), $(this).data("active", false)) : (block.css("display", "block"), block.data("active", true))
		}),
		document.title = block.data("title"),
		$(".menu-item a").each(function() {
			$(this).removeClass("active")
		}),
		b.addClass("active"),
		a = "";
		a && (a = treeio.prepare_url(a), $("#loading-status").css("display", "block"), $("#loading-status-text").html("Loading..."), $.ajax({
			url: a,
			dataType: "json",
			success: treeio.process_ajax,
			complete: treeio.process_html,
			error: treeio.show_error
		}))
	},
	show_error: function() {
		$("#loading-status-text").html("Something went wrong...")
	},
	process_userblock: function(a) {
		a.response.messages && $("#userblock-messages").each(function() {
			$(this).html(a.response.messages)
		})
	},
	process_ajax: function(a) {
		if (a) if (a.popup) treeio.process_popup_data(a);
		else if (a.redirect) window.location.hash == "#" + a.redirect ? treeio.do_ajax() : window.location.hash = a.redirect;
		else if (a.redirect_out) window.location = a.redirect_out;
		else {
			if (a.response.url) {
				var b = a.response.url.replace(".ajax", ""),
				c = window.location.hash.replace("#", "");
				if (b != c && b.indexOf(c) == - 1 && c.indexOf(b) == - 1) {
					$("#loading-status").css("display", "none");
					return
				}
			}
			document.title = a.response.content.title;
			var b = a.response.content.module_content,
			c = a.response.modules.active,
			d = "none";
			if ($("#module-" + c).length == 0) $("#content").append('<div class="module-block" id="module-' + c + '"></div>');
			else {
				var f = $("td.module-sidebar-right", $("#module-" + c));
				f && (d = f.css("display"))
			}
			var h = $("#module-" + c);
			$(".module-block").each(function() {
				$(this).attr("id") != h.attr("id") ? ($(this).css("display", "none"), $(this).data("active", false)) : (h.css("display", "block"), h.data("active", true))
			});
			treeio.remove_mce($("#module-" + c + " form"));
			$("#module-" + c).html(b);
			$("#module-" + c + " form").length && (treeio.prepare_forms(h), treeio.prepare_comments(h), $("#module-" + c + " textarea").length && treeio.put_mce(h));
			treeio.prepare_tags(h);
			treeio.prepare_list_actions(h);
			treeio.prepare_attachments(h);
			treeio.prepare_invites(h);
			treeio.prepare_popups(h);
			treeio.convert_links(h);
			treeio.prepare_ajax_links(h);
			treeio.prepare_slider_sidebar(h, d);
			treeio.showhidejs(h);
			treeio.prepare_module_stuff(c);
			treeio.process_notifications(a.response.notifications);
			$(".menu-item a").each(function() {
				$(this).removeClass("active")
			});
			treeio.process_userblock(a);
			$("#menu-" + c).addClass("active");
			$(h).data("title", a.response.content.title);
			$("#loading-splash").css("display") != "none" && $("#loading-splash").fadeOut();
			$("#loading-status").css("display", "none")
		}
	},
	process_notifications: function(a) {
		for (var b in a) {
			var c = {
				title: " ",
				text: a[b].message,
				image: "/static/notifications/" + a[b].tags + ".png"
			};
			if (a[b].title) c.title = a[b].title;
			if (a[b].image) c.image = a[b].image;
			$.gritter.add(c)
		}
	},
	process_html: function(a, b) {
		b == "parsererror" && window.document.write(a.responseText)
	},
	prepare_module_stuff: function(a) {
		try {
			treeio.modules[a].init()
		} catch(b) {}
	},
	prepare_url: function(a) {
		if (a.indexOf("!") != - 1 || a.indexOf("?") != - 1) a = a.replace("!", "?"),
		a.indexOf(".ajax") == - 1 && (a = a.replace("?", ".ajax?"));
		a.indexOf(".ajax") == - 1 && (a += ".ajax?");
		return a
	},
	showhidejs: function(a) {
		if (a) var b = $("div.showjs", a),
		a = $("div.hidejs", a);
		else b = $("div.showjs"),
		a = $("div.hidejs");
		b.each(function() {
			$(this).css("display", "block")
		});
		a.each(function() {
			$(this).css("display", "none")
		})
	},
	convert_links: function(a) { (a ? $("a", a) : $("a")).each(function() {
			if ($(this).attr("href") && ! $(this).hasClass("ajax-link-out") && ! $(this).hasClass("ajax-link") && ! $(this).attr("target") && $(this).attr("href").substring(0, 3) != "www" && $(this).attr("href").substring(0, 5) != "http:" && $(this).attr("href").substring(0, 6) != "https:" && $(this).attr("href").substring(0, 4) != "ftp:" && $(this).attr("href").substring(0, 7) != "mailto:" && $(this).attr("href").indexOf("#") == - 1 && ($(this).attr("href", "#" + $(this).attr("href").replace("?", "!")), $.browser.msie && $.browser.version.substr(0, 1) < 7)) {
				var a = window.location.href.replace(window.location.hash, "");
				$(this).attr("href", $(this).attr("href").replace(a, ""))
			}
		})
	},
	add_data: function(a) {
		var b = $(a.target);
		a.inner ? b.html(a.content) : a.append ? b.append(a.content) : (a = $(a.content), b.replaceWith(a), b = a);
		$("form", b).length && (treeio.prepare_forms(b), treeio.prepare_comments(b), $("textarea", b).length && treeio.put_mce(b));
		treeio.prepare_tags(b);
		treeio.prepare_list_actions(b);
		treeio.prepare_attachments(b);
		treeio.prepare_invites(b);
		treeio.prepare_popups(b);
		treeio.convert_links(b);
		treeio.prepare_ajax_links(b);
		treeio.showhidejs(b);
		$("#loading-status").css("display", "none")
	},
	prepare_ajax_links: function(a) { (a ? $(".ajax-link", a) : $(".ajax-link")).each(function() {
			$(this).click(function() {
				var a = $(this).parents($(this).attr("target")),
				c = treeio.utils.generate_id();
				a.attr("id", c);
				$(this).attr("target", "#" + c);
				var a = eval($(this).attr("callback")),
				d = eval("(" + $(this).attr("args") + ")"),
				c = d ? $.extend({
					target: "#" + c
				},
				d) : {
					target: "#" + c
				};
				$("#loading-status").css("display", "block");
				$("#loading-status-text").html("Loading...");
				a(Dajax.process, c);
				return false
			})
		})
	},
	prepare_slider_sidebar: function(a, b) {
		a || (a = $(".module-block"));
		var c = $("<div></div>").addClass("sidebar-slider");
		$("td.module-content-inner", a).prepend(c);
		c.data("sidebar", $("td.module-sidebar-right", a));
		c.click(function() {
			var a = $(this).data("sidebar");
			a && (a.css("display") == "none" ? a.fadeIn() : a.fadeOut())
		});
		var d = $("td.module-sidebar-right", a);
		($("a.projects-action", d).length != 0 || $("a.services-action", d).length != 0) && c.append('<img src="/static/icons/sidebar/status.gif"/><br />');
		$("form.content-filter-form", d).length != 0 && c.append('<img src="/static/icons/sidebar/filter.gif"/><br />');
		$("div.permission-links", d).length != 0 && c.append('<img src="/static/icons/sidebar/permission.gif"/><br />');
		$("div.object-links", d).length != 0 && c.append('<img src="/static/icons/sidebar/link.gif"/><br />');
		$("div.subscription-users", d).length != 0 && c.append('<img src="/static/icons/sidebar/subscribe.gif"/><br />');
		$("a.pdf-block-link", d).length != 0 && c.append('<img src="/static/icons/sidebar/export.gif"/><br />');
		b ? d.css("display", b) : (d.css("display", "none"), c.css({
			visibility: "hidden"
		}))
	},
	prepare_list_actions: function(a) {
		$(".content-list-item", a).each(function() {
			$("span.content-list-item-actions", $(this)).css("visibility", "hidden");
			$(this).mouseover(function() {
				$("span.content-list-item-actions", $(this)).css("visibility", "visible")
			}).mouseout(function() {
				$("span.content-list-item-actions", $(this)).css("visibility", "hidden")
			});
			$("span.content-list-item-actions a", $(this)).addClass("popup-link")
		})
	},
	put_datepicker: function(a) {
		$("input.datepicker", a).each(function() {
			var a = {},
			c = $(this).attr("initial");
			if (c) c = parseInt(c) * 1E3,
			a.defaultDate = new Date(c);
			$(this).datepicker(a)
		});
		$("input.datetimepicker", a).each(function() {
			var a = {
				stepMinute: 5,
				hour: 12,
				minute: 0,
				firstDay: 1
			},
			c = $(this).attr("initial");
			if (c) c = parseInt(c) * 1E3,
			c = new Date(c),
			a.defaultDate = c,
			a.hour = c.getHours(),
			a.minute = c.getMinutes(),
			a.second = c.getSeconds();
			$(this).datetimepicker(a)
		})
	},
	prepare_mass_form: function(a) {
		$("input[type=checkbox].group-control", a).each(function() {
			$(this).data("form", $("ul.mass-form", a));
			$(this).click(function() {
				$("input[type=checkbox].group-" + $(this).attr("name")).attr("checked", $(this).attr("checked"));
				$(this).data("form").fadeTo("fast", 1)
			})
		});
		$("ul.mass-form input[type=submit]", a).remove();
		$("ul.mass-form", a).each(function() {
			$(this).css("opacity", 0.6)
		});
		$(".content-list-item input[type=checkbox], #sales_table, #reports_table", a).each(function() {
			$(this).data("form", $("ul.mass-form", a));
			$(this).click(function() {
				$(this).data("form").fadeTo("fast", 1)
			})
		});
		$(".mass-form select", a).each(function() {
			$(this).css("opacity", 0);
			$(this).change(function() {
				var a = $("span.wrap-value", $(this).parent()),
				c = $(this).children("option:selected"); ! c.val() == "" && (a.text(c.text()), c.val() == "delete" || c.val() == "delete_all" ? confirm("Really delete?\n\n(This cannot be undone)") && $(this).parent().submit() : $(this).parent().submit())
			})
		});
		$(".mass-form label", a).each(function() {
			$(this).next("select").andSelf().wrapAll('<div class="wrap-class" />');
			$(this).replaceWith('<span class="wrap-label">' + $(this).text() + '&nbsp;<span class="wrap-value"></span></span>')
		})
	},
	prepare_filter_form: function(a) {
		$("form.content-filter-form input", a).live("change", function() {
			$(this).parents("form.content-filter-form").submit()
		});
		$("form.content-filter-form select", a).live("change", function() {
			$(this).parents("form.content-filter-form").submit()
		});
		$("form.content-filter-form :submit").hide()
	},
	prepare_popup_content: function(a) {
		var b = a.popup_id;
		if ($("#" + b).length) {
			var c = $("#" + b);
			$("a", c).each(function() {
				if ($(this).attr("href") && ! $(this).hasClass("popup-link") && ! $(this).hasClass("ajax-link-out") && ! $(this).attr("target") && $(this).attr("href").substring(0, 3) != "www" && $(this).attr("href").substring(0, 5) != "http:" && $(this).attr("href").substring(0, 6) != "https:" && $(this).attr("href").substring(0, 4) != "ftp:" && $(this).attr("href").substring(0, 7) != "mailto:") {
					$(this).attr("href").indexOf(b) == - 1 ? $(this).data("href", "/user/popup/" + b + "/url=" + $(this).attr("href")) : $(this).data("href", $(this).attr("href"));
					if ($.browser.msie && $.browser.version.substr(0, 1) < 7) {
						var a = window.location.href.replace(window.location.hash, "");
						$(this).data("href", $(this).data("href").replace(a, "/"))
					}
					$(this).click(function() {
						$("#loading-status").css("display", "block");
						url = $(this).data("href");
						$.ajax({
							url: url,
							dataType: "json",
							success: treeio.process_popup_data
						});
						return false
					})
				}
			});
			treeio.prepare_popups(c);
			$("form", c).each(function() { (url = $(this).attr("action")) ? url.indexOf("/user/popup/") == - 1 && (url = "/user/popup/" + a.popup_id + "/url=" + url) : url = a.url;
				$(this).attr("action", url);
				var b = {
					beforeSubmit: function() {
						$("#loading-status").css("display", "block")
					},
					url: url,
					dataType: "json",
					success: treeio.process_ajax
				};
				$(this).ajaxForm(b)
			});
			treeio.showhidejs(c);
			treeio.prepare_ajax_links(c);
			treeio.prepare_comments(c);
			treeio.prepare_attachments(c);
			treeio.prepare_invites(c);
			treeio.prepare_tags(c);
			treeio.prepare_autocomplete(c);
			treeio.prepare_search_duplicates(c);
			treeio.put_datepicker(c);
			treeio.prepare_mass_form(c);
			treeio.put_mce(c)
		}
	},
	process_popup_data: function(a) {
		if (a.popup) {
			var b = $("#" + a.popup.popup_id);
			if (a.popup.object) {
				if (b.data("field")) {
					var c = $("#" + b.data("module")),
					d = $("#" + b.data("field"), c);
					d.hasClass("autocomplete") ? (d.val(a.popup.object.name), c = $("#" + d.attr("id").replace("autocomplete_", ""), c), c.each(function() {
						$(this).val(a.popup.object.id)
					})) : d.hasClass("duplicates") ? (d.val(a.popup.object.name), c = $("#" + d.attr("id").replace("duplicates_", ""), c), c.each(function() {
						$(this).val(a.popup.object.id)
					})) : d.append('<option value="' + a.popup.object.id + '" selected="selected">' + a.popup.object.name + "</option>")
				} else {
					var f = location.hash.substring(1),
					f = treeio.prepare_url(f),
					c = b.parents("div.popup-block-inner");
					$("#loading-status").css("display", "block");
					c.length > 0 && $(c).first().each(function() {
						f = "/user/popup/" + $(this).attr("id") + "/url=" + $(this).parent().data("link").replace("#", "")
					});
					$.ajax({
						url: f,
						dataType: "json",
						success: treeio.process_ajax,
						complete: treeio.process_html
					})
				}
				b.parent().remove()
			} else a.popup.redirect ? (f = location.hash.substring(1), f = treeio.prepare_url(f), c = b.parents("div.popup-block-inner"), $("#loading-status").css("display", "block"), c.length > 0 && $(c).first().each(function() {
				f = "/user/popup/" + $(this).attr("id") + "/url=" + $(this).parent().data("link").replace("#", "")
			}), $.ajax({
				url: f,
				dataType: "json",
				success: treeio.process_ajax,
				complete: treeio.process_html
			}), b.parent().remove()) : (c = b.parent().children("div.popup-title-block"), c.children("span.popup-title").html(a.popup.title), c.children("span.popup-subtitle").html(a.popup.subtitle), b.html(a.popup.content), treeio.prepare_popup_content(a.popup), b.parent().fadeIn(300), $("input:text:visible:first", b).focus())
		}
		$("#loading-status").css("display", "none")
	},
	prepare_popups: function(a) {
		$("a.popup-link", a).each(function() {
			$(this).hasClass("popup-link-out") || $(this).click(function() {
				var b = a.attr("id") + "-popup-" + $(this).attr("id") + "-" + Date.now();
				if ($("#" + b).length) return false;
				$("#loading-status").css("display", "block");
				var c = $("<div></div>").addClass("popup-block").css("display", "none").css("visibility", "visible");
				c.data("link", $(this).attr("href"));
				var d = $("<div></div>").addClass("popup-title-block");
				d.append($("<span></span>").addClass("popup-title"));
				d.append($("<span></span>").addClass("popup-subtitle"));
				var f = $("<div></div>").addClass("popup-link-open");
				f.click(function() {
					var a = $(this).parent().data("link");
					if (a) a = a.replace("#", ""),
					window.location.hash = a,
					$(this).parent().remove()
				});
				var h = $("<div></div>").addClass("popup-close");
				h.click(function() {
					$("#" + b).length && $("#" + b).parent().remove()
				});
				var n = $("<div></div>").addClass("popup-block-inner");
				n.attr("id", b);
				$(this).attr("field") && (n.data("field", $(this).attr("field")), n.data("module", a.attr("id")));
				c.append(h);
				c.append(f);
				c.append(d);
				c.append(n);
				a.append(c);
				d = c.parents("div.popup-block-inner");
				d.length > 0 ? (d = d.first().offset(), c.position({
					my: "center top",
					at: "center top",
					of: $(this),
					collision: "flip",
					offset: "-" + d.left + " -" + d.top + ""
				})) : c.position({
					my: "left top",
					at: "left top",
					of: $(this),
					collision: "fit",
					offset: "-30 -5"
				});
				c.draggable({
					handle: "div.popup-title-block",
					opacity: 0.5,
					addClasses: false
				});
				url = "/user/popup/" + b + "/url=" + $(this).attr("href").replace("#", "");
				$.browser.msie && $.browser.version.substr(0, 1) < 7 && (url = "/user/popup/" + b + "/url=/" + $(this).attr("href").replace("#", ""), c = window.location.href.replace(window.location.hash, ""), url = url.replace(c, ""));
				url = url.replace("//", "/");
				$.ajax({
					url: url,
					dataType: "json",
					success: treeio.process_popup_data
				});
				return false
			})
		})
	},
	prepare_autocomplete: function(a) {
		$("input.autocomplete", a).each(function() {
			$(this).data("hidden_field", $("#id_" + $(this).attr("name").replace("autocomplete_", ""), a));
			$(this).autocomplete({
				source: $(this).attr("callback") + ".json",
				focus: function(a, c) {
					$(this).val(c.item.label);
					$(this).data("hidden_field").val(c.item.value);
					return false
				},
				select: function(a, c) {
					$(this).val(c.item.label);
					$(this).data("hidden_field").val(c.item.value);
					return false
				}
			});
			$(this).change(function() {
				$(this).val() == "" && $(this).data("hidden_field").val("")
			})
		});
		$("input.multicomplete", a).each(function() {
			$(this).data("hidden_fields", $("#" + $(this).attr("name").replace("multicomplete_", "multi_"), a));
			$(this).bind("keydown", function(a) {
				a.keyCode === $.ui.keyCode.TAB && $(this).data("autocomplete").menu.active && a.preventDefault()
			});
			$(this).bind("keyup", function(a) {
				if (a.keyCode === $.ui.keyCode.BACKSPACE || a.keyCode === $.ui.keyCode.DELETE) for (var a = treeio.utils.split(this.value), b = $("input", $(this).data("hidden_fields")), f = 0; f < b.length; f++) {
					var h = $(b[f]).attr("label");
					$.inArray(h, a) == - 1 && $(b[f]).remove()
				}
			});
			var b = $(this).attr("callback") + ".json";
			$(this).autocomplete({
				source: function(a, d) {
					$.getJSON(b, {
						term: treeio.utils.extractLast(a.term)
					},
					d)
				},
				search: function() {
					if (treeio.utils.extractLast(this.value).length < 2) return false
				},
				focus: function() {
					return false
				},
				select: function(a, b) {
					var f = treeio.utils.split(this.value);
					f.pop();
					f.push(b.item.label);
					f.push("");
					var h = $(this).data("hidden_fields"),
					n = $("<input>");
					n.attr("type", "hidden").attr("name", $(this).attr("name").replace("multicomplete_", "")).attr("id", "id_" + n.attr("name")).attr("value", b.item.value).attr("label", b.item.label);
					this.value = f.join(", ");
					h.append(n);
					f = treeio.utils.split(this.value);
					h = $("input", $(this).data("hidden_fields"));
					for (n = 0; n < h.length; n++) {
						var g = $(h[n]).attr("label");
						$.inArray(g, f) == - 1 && $(h[n]).remove()
					}
					return false
				}
			})
		})
	},
	prepare_search_duplicates: function(a) {
		$("input.duplicates", a).each(function() {
			$(this).data("hidden_field", $("#id_" + $(this).attr("name").replace("duplicates_", ""), a));
			$(this).autocomplete({
				source: $(this).attr("callback") + ".json",
				focus: function(a, c) {
					$(this).val(c.item.label);
					return false
				},
				select: function(a, c) {
					$(this).val(c.item.label);
					return false
				}
			})
		})
	},
	prepare_attachments: function(a) {
		$(".delete-attachment", a).each(function() {
			$(this).click(function() {
				Dajaxice.treeio.account.attachment_delete(Dajax.process, {
					attachment_id: $(this).attr("attachment")
				});
				return false
			})
		});
		$(".attachment-uploader", a).each(function() {
			new qq.FileUploader({
				action: $(this).attr("action"),
				element: this,
				multiple: false,
				onComplete: function(a, c, d) {
					Dajaxice.treeio.account.attachment(Dajax.process, {
						object_id: d.object_id,
						update_id: d.update_id
					})
				},
				onAllComplete: function() {},
				params: {
					csrf_token: $(this).attr("csrf"),
					csrf_name: "csrfmiddlewaretoken",
					csrf_xname: "X-CSRFToken"
				},
				text: treeio_attachment_text
			})
		});
		$(".attachment-record-uploader", a).each(function() {
			new qq.FileUploader({
				action: $(this).attr("action"),
				element: this,
				multiple: false,
				onComplete: function(a, c, d) {
					Dajaxice.treeio.account.attachment(Dajax.process, {
						object_id: d.object_id,
						update_id: d.update_id
					})
				},
				onAllComplete: function() {},
				params: {
					csrf_token: $(this).attr("csrf"),
					csrf_name: "csrfmiddlewaretoken",
					csrf_xname: "X-CSRFToken"
				},
				text: treeio_attachment_record_text
			})
		})
	},
	prepare_invites: function(a) {
		$(".easy-invite", a).each(function() {
			$(this).click(function() {
				Dajaxice.treeio.account.easy_invite(Dajax.process, {
					emails: $(this).attr("emails")
				});
				return false
			})
		})
	},
	prepare_comments: function(a) {
		$("a.like-button", a).each(function() {
			$(this).click(function() {
				$(this).parent().submit();
				return false
			})
		});
		$("a.comment-button", a).each(function() {
			$(this).click(function() {
				var a = $("div.comments-likes-box-" + $(this).attr("object"));
				a.toggle();
				a.css("display") != "none" && $("textarea:visible:first", a).focus();
				return false
			})
		});
		$("span.comments-likes-toggle", a).each(function() {
			$(this).click(function() {
				var a = $("div.comments-likes-box-" + $(this).attr("object"));
				a.toggle();
				a.css("display") != "none" && $("textarea:visible:first", a).focus();
				return false
			})
		});
		$("form.like-form", a).each(function() {
			var a = "comments-likes-box-" + $(this).attr("object");
			$("#" + a);
			$(this).attr("target", a);
			$(this).submit(function() {
				var a = $(this).attr("target"),
				b = $(this).parents("#" + a),
				a = treeio.utils.generate_id(a);
				b.attr("id", a);
				a = {
					target: "#" + a,
					form: $(this).serializeObject(),
					expand: true
				};
				Dajaxice.treeio.account.comments_likes(Dajax.process, a);
				return false
			})
		})
	},
	prepare_tags: function(a) {
		$("input#id_multicomplete_tags", a).each(function() {
			$(this).focus();
			$(this).focusout(function() {
				$(this).parent("form").submit()
			});
			$(this).parent("form").submit(function() {
				var a = $(this).attr("target"),
				c = $(this).parents(a),
				a = treeio.utils.generate_id();
				c.attr("id", a);
				a = {
					target: "#" + a,
					object_id: $(this).attr("object"),
					edit: true,
					formdata: $(this).serializeObject()
				};
				Dajaxice.treeio.account.tags(Dajax.process, a);
				return false
			})
		});
		$("span.tags-box").each(function() {
			$("span.tags-box-link", $(this)).css("visibility", "hidden");
			$(this).hover(function() {
				$("span.tags-box-link", $(this)).css("visibility", "visible")
			},
			function() {
				$("span.tags-box-link", $(this)).css("visibility", "hidden")
			})
		})
	},
	prepare_forms: function(a) {
		$("form", a).each(function() {
			if (!$(this).hasClass("like-form") && ! $(this).hasClass("tags-form")) { (url = $(this).attr("action")) || (url = location.hash.substring(1));
				if ($(this).attr("method") == "get") {
					$(this).attr("action", url);
					var a = {
						beforeSubmit: function(a, b) {
							var f = b.attr("action");
							f.indexOf("!") != - 1 && (f = f.substring(0, f.indexOf("!")));
							f += "!" + b.formSerialize();
							window.location.hash = "#" + f;
							return false
						}
					}
				} else url = treeio.prepare_url(url),
				a = {
					beforeSubmit: function() {
						$("#loading-status").css("display", "block")
					},
					url: url,
					dataType: "json",
					success: treeio.process_ajax
				};
				$(this).ajaxForm(a)
			}
		});
		treeio.prepare_mass_form(a);
		treeio.prepare_filter_form(a);
		treeio.prepare_autocomplete(a);
		treeio.prepare_search_duplicates(a);
		treeio.put_datepicker(a)
	},
	prepare_dropdown_menus: function() {
		$("a.menu-dropdown-link").each(function() {
			$(this).click(function() {
				var a = $("#" + $(this).attr("dropdown"));
				$(this).addClass("menu-dropdown-link-active");
				a.slideDown("fast").show()
			});
			$(this).hover(function() {
				var a = $("#" + $(this).attr("dropdown"));
				$(this).addClass("menu-dropdown-link-active");
				a.slideDown("fast").show()
			});
			$(this).parent().hover(function() {},
			function() {
				var a = $(this).children("a.menu-dropdown-link");
				$(this).children("#" + a.attr("dropdown")).slideUp("fast");
				a.removeClass("menu-dropdown-link-active")
			})
		})
	},
	prepare_toolbar: function() {
		$("span.hide_toolbar").click(function() {
			$("#toolbar").slideToggle("fast", function() {
				$("#toolbar_action").fadeIn("slow")
			})
		});
		$("span.show_toolbar").click(function() {
			$("#toolbar_action").fadeOut("fast", function() {
				$("#toolbar").slideToggle("fast")
			})
		})
	}
};
treeio.utils = {
	split: function(a) {
		return a.split(/,\s*/)
	},
	extractLast: function(a) {
		return treeio.utils.split(a).pop()
	},
	generate_id: function(a) {
		a || (a = "ajax");
		for (var a = a + "-" + Date.now(), b = 0; $("#" + a).length > 0;) a = a + "-" + b,
		b++;
		return a
	}
};
treeio.modules = {
	"treeio-home": {
		init: function() {
			var a = {
				opacity: 0.6,
				handle: "div.widget-title",
				connectWith: "#widget-panel-right",
				items: "div.widget-block",
				cursor: "move",
				update: function() {
					var a = $(this).attr("callback") + "?" + $(this).sortable("serialize");
					$.ajax({
						url: a
					})
				},
				start: function(a, c) {
					$("#widget-panel-left").addClass("widget-panel-active");
					$("#widget-panel-right").addClass("widget-panel-active");
					c.item.addClass("widget-block-moving")
				},
				beforeStop: function(a, c) {
					c.item.removeClass("widget-block-moving")
				},
				stop: function() {
					$("#widget-panel-left").removeClass("widget-panel-active");
					$("#widget-panel-right").removeClass("widget-panel-active")
				}
			};
			$("#widget-panel-left").sortable(a);
			a.connectWith = "#widget-panel-left";
			$("#widget-panel-right").sortable(a)
		}
	},
	"treeio-core": {
		init: function() {
			$("div.setup-module-box").length > 0 && $("div.setup-module-box").each(function() {
				$(this).click(function() {
					$(this).toggleClass("setup-module-box-active");
					$("input", $(this)).each(function() {
						$(this).attr("checked", ! $(this).attr("checked"))
					})
				})
			})
		}
	},
	"treeio-projects": {
		timer: function() {
			var a = $(".projects-timeslot");
			a && (a.each(function() {
				var a = $(this).data("start"),
				c = Date.now();
				a == null && (a = parseInt($(this).attr("diff")), a = c - a * 1E3, $(this).data("start", a));
				var d = (c - a) / 1E3,
				a = Math.floor(d / 3600),
				c = Math.floor((d / 3600 - a) * 60),
				d = Math.round(((d / 3600 - a) * 60 - c) * 60);
				a += ":";
				a += c >= 10 ? c + ":": "0" + c + ":";
				a += d >= 10 ? d: "0" + d;
				$(this).html(a)
			}), window.setTimeout(treeio.modules["treeio-projects"].timer, 1E3))
		},
		init: function() {
			$(".projects-timeslot") && this.timer();
			var a = $("div.ganttChart");
			a && this.gantt(a)
		},
		gantt: function(a) {
			a.each(function() {
				if (ganttData) {
					$(this).ganttView({
						data: ganttData,
						behavior: {
							onClick: function() {},
							onResize: function(a) {
								Dajaxice.treeio.projects.gantt(callback_function, {
									task: a.id,
									start: a.start.toString("yyyy-M-d"),
									end: a.end.toString("yyyy-M-d")
								})
							},
							onDrag: function(a) {
								Dajaxice.treeio.projects.gantt(callback_function, {
									task: a.id,
									start: a.start.toString("yyyy-M-d"),
									end: a.end.toString("yyyy-M-d")
								})
							}
						}
					});
					var a = $("#module-treeio-projects");
					$(this).ganttView("setSlideWidth", $("td.module-content", a).width() - 60);
					treeio.prepare_popups($(this));
					$(window).resize(function() {
						$("div.ganttChart", a).each(function() {
							var a = $("#module-treeio-projects");
							$(this).ganttView("setSlideWidth", $("td.module-content", a).width() - 60)
						})
					})
				}
			})
		}
	},
	"treeio-reports": {
		init: function() {}
	}
};
treeio.nuvius = {
	profile: null,
	access_popup: false,
	reload_on_profile: true,
	fetch_profile: function() {
		$("#loading-status").css("display", "block");
		$("#loading-status-text").html("Loading...");
		$.ajax({
			url: nuvius_profile_url,
			dataType: "jsonp",
			success: treeio.nuvius.load_profile,
			error: treeio.show_error
		})
	},
	check_profile: function(a) {
		a ? a.key_valid && (a.username ? $("#nuvius-username").html(a.username) : $("#nuvius-username").html("Anonymous User"), treeio.nuvius.reload_on_profile && treeio.do_ajax()) : treeio.nuvius.profile && (a = nuvius_profile_check_url, a += "?nuvius_id=" + treeio.nuvius.profile.id + "&profile_key=" + treeio.nuvius.profile.key, $.ajax({
			url: a,
			dataType: "json",
			success: treeio.nuvius.check_profile,
			error: treeio.show_error
		}))
	},
	load_profile: function(a) {
		$("#loading-status").css("display", "none");
		if (a.profile) ! a.profile.access_granted && treeio.nuvius.access_popup ? ($.colorbox({
			href: a.profile.access_url,
			width: "80%",
			height: "80%",
			iframe: true,
			overlayClose: false,
			onClosed: treeio.nuvius.fetch_profile
		}), treeio.nuvius.access_popup = false) : (treeio.nuvius.profile = a.profile, treeio.nuvius.check_profile())
	},
	fetch_access: function() {
		treeio.nuvius.access_popup = true;
		treeio.nuvius.fetch_profile()
	},
	close_iframe: function() {
		$.colorbox.close()
	}
};
$(function() {
	$(window).hashchange(treeio.do_ajax);
	$(window).hashchange();
	treeio.prepare_dropdown_menus();
	treeio.prepare_toolbar();
	treeio.convert_links();
	treeio.prepare_ajax_links();
	$(".menu-item a").each(function() {
		$(this).click(function() {
			$(this).hasClass("active") && $(this).attr("href") == window.location.hash && $(window).hashchange()
		})
	});
	$("#perspective_switch").each(function() { (url = $(this).attr("action")) || (url = location.hash.substring(1));
		url = treeio.prepare_url(url);
		var a = {
			beforeSubmit: function() {
				$("#loading-status").css("display", "block")
			},
			url: url,
			dataType: "json",
			success: treeio.process_ajax
		};
		$(this).ajaxForm(a);
		$(this).children("select").change(function() {
			$("#perspective_switch").submit()
		})
	});
	$("form#search_form").each(function() { (url = $(this).attr("action")) || (url = location.hash.substring(1));
		$(this).attr("action", url);
		$(this).ajaxForm({
			beforeSubmit: function(a, b) {
				var c = b.attr("action");
				c += "!" + b.formSerialize();
				window.location.hash = "#" + c;
				return false
			}
		})
	});
	$(".module-block").data("title", document.title);
	$(".module-block").each(function() {
		doc = $(this);
		$("form").length && (treeio.prepare_forms(doc), treeio.prepare_comments(doc), $("textarea").length && treeio.put_mce(doc), treeio.put_datepicker(doc), treeio.prepare_forms(doc));
		treeio.prepare_tags();
		treeio.prepare_slider_sidebar(doc);
		treeio.prepare_list_actions(doc);
		treeio.prepare_attachments(doc);
		treeio.prepare_invites(doc);
		treeio.prepare_popups(doc);
		treeio.showhidejs(doc);
		module_name = $(this).attr("id").substring(7);
		treeio.prepare_module_stuff(module_name);
		window.setTimeout("$('#loading-splash').fadeOut();", 5E3)
	})
});
(function(a) {
	a.flexbox = function(b, c) {
		function d(a, b) {
			M && clearTimeout(M);
			M = setTimeout(function() {
				f(1, a, "")
			},
			b ? c.queryDelay * 5: c.queryDelay)
		}
		function f(b, d, g) {
			d && (g = "");
			var f = g && g.length > 0 ? g: a.trim(G.val());
			f.length >= c.minChars || d ? (L.outerHeight() > 0 && L.css("height", L.outerHeight()), L.html("").attr("scrollTop", 0), (d = j(f, b)) ? (m(d.data, f), n(b, d.t)) : (d = {
				q: f,
				p: b,
				s: x,
				contentType: "application/json; charset=utf-8"
			},
			g = function(a, d) {
				d === true && (f = d);
				var g = parseInt(a[c.totalProperty]);
				if (isNaN(g) && c.paging) {
					c.maxCacheBytes <= 0 && alert('The "maxCacheBytes" configuration option must be greater\nthan zero when implementing client-side paging.');
					var g = a[c.resultsProperty].length,
					j = g / x;
					g % x > 0 && (j = parseInt(++j));
					for (var h = 1; h <= j; h++) {
						var p = {};
						p[c.totalProperty] = g;
						p[c.resultsProperty] = a[c.resultsProperty].splice(0, x);
						h === 1 && (q = m(p, f));
						o(f, h, x, g, p, q)
					}
				} else {
					var q = m(a, f);
					o(f, b, x, g, a, q)
				}
				n(b, g)
			},
			typeof c.source === "object" ? c.allowInput ? g(h(c.source, d)) : g(c.source) : c.method.toUpperCase() == "POST" ? a.post(c.source, d, g, "json") : a.getJSON(c.source, d, g))) : q()
		}
		function h(a, b) {
			var d = {};
			d[c.resultsProperty] = [];
			for (var g = d[c.totalProperty] = 0, f = 0; f < a[c.resultsProperty].length; f++) a[c.resultsProperty][f].name.toLowerCase().indexOf(b.q.toLowerCase()) === 0 && (d[c.resultsProperty][g++] = a[c.resultsProperty][f], d[c.totalProperty] += 1);
			c.paging && (g = (b.p - 1) * b.s, d[c.resultsProperty] = d[c.resultsProperty].splice(g, g + b.s > d[c.totalProperty] ? d[c.totalProperty] - g: b.s));
			return d
		}
		function n(a, b) {
			U.html("").removeClass(c.paging.cssClass);
			if (c.showResults && c.paging && b > x) {
				var d = b / x;
				b % x > 0 && (d = parseInt(++d));
				p(d, a, b)
			}
		}
		function g() {
			f(parseInt(a(this).attr("page")), true, G.attr("pq"));
			return false
		}
		function p(b, d, j) {
			U.addClass(c.paging.cssClass);
			var h = a("<a/>").attr("href", "#").addClass("page").click(g),
			p = a("<span></span>").addClass("page"),
			n = ha.attr("id");
			d > 1 ? (h.clone(true).attr("id", n + "f").attr("page", 1).html("&lt;&lt;").appendTo(U), h.clone(true).attr("id", n + "p").attr("page", d - 1).html("&lt;").appendTo(U)) : (p.clone(true).html("&lt;&lt;").appendTo(U), p.clone(true).html("&lt;").appendTo(U));
			if (c.paging.style === "links") {
				var o = c.paging.maxPageLinks;
				if (b <= o) for (var m = 1; m <= b; m++) m === d ? p.clone(true).html(d).appendTo(U) : h.clone(true).attr("page", m).html(m).appendTo(U);
				else {
					startPage = d + parseInt(o / 2) > b ? b - o + 1: d - parseInt(o / 2);
					startPage > 1 ? h.clone(true).attr("page", startPage - 1).html("...").appendTo(U) : startPage = 1;
					for (m = startPage; m < startPage + o; m++) m === d ? p.clone(true).html(m).appendTo(U) : h.clone(true).attr("page", m).html(m).appendTo(U);
					b > startPage + o && h.clone(true).attr("page", m).html("...").appendTo(U)
				}
			} else c.paging.style === "input" && a("<input/>").addClass("box").click(function() {
				this.select()
			}).keypress(function(c) {
				var d = this.value;
				if (/^13$|^39$|^37$/.test(c.keyCode)) switch (c.preventDefault && c.preventDefault(), c.stopPropagation && c.stopPropagation(), c.cancelBubble = true, c.returnValue = false, c.keyCode) {
				case 13:
					/^\d+$/.test(d) && d > 0 && d <= b ? f(d, true) : alert("Please enter a page number between 1 and " + b);
					break;
				case 39:
					a("#" + ha.attr("id") + "n").click();
					break;
				case 37:
					a("#" + ha.attr("id") + "p").click()
				}
			}).val(d).appendTo(U);
			d < b ? (h.clone(true).attr("id", n + "n").attr("page", + d + 1).html("&gt;").appendTo(U), h.clone(true).attr("id", n + "l").attr("page", b).html("&gt;&gt;").appendTo(U)) : (p.clone(true).html("&gt;").appendTo(U), p.clone(true).html("&gt;&gt;").appendTo(U));
			h = (d - 1) * x + 1;
			p = h > j - x ? j: h + x - 1;
			c.paging.showSummary && (d = c.paging.summaryTemplate.applyTemplate({
				start: h,
				end: p,
				total: j,
				page: d,
				pages: b
			}), a("<br/>").appendTo(U), a("<span></span>").addClass(c.paging.summaryClass).html(d).appendTo(U))
		}
		function j(a, b) {
			var c = a + N + b;
			if (A[c]) for (var d = 0; d < Q.length; d++) if (Q[d] === c) return Q.unshift(Q.splice(d, 1)[0]),
			A[c];
			return false
		}
		function o(a, b, d, g, f, j) {
			if (c.maxCacheBytes > 0) {
				for (; Q.length && v + j > c.maxCacheBytes;) {
					var h = Q.pop();
					v -= h.size
				}
				h = a + N + b;
				A[h] = {
					q: a,
					p: b,
					s: d,
					t: g,
					size: j,
					data: f
				};
				Q.push(h);
				v += j
			}
		}
		function m(b, d) {
			var g = 0,
			f = 0;
			if (b) if (parseInt(b[c.totalProperty]) === 0 && c.noResultsText && c.noResultsText.length > 0) L.addClass(c.noResultsClass).html(c.noResultsText),
			P.show();
			else {
				L.removeClass(c.noResultsClass);
				for (var j = 0; j < b[c.resultsProperty].length; j++) {
					var h = b[c.resultsProperty][j],
					p = c.resultTemplate.applyTemplate(h),
					n = d === p,
					o = false,
					m = false,
					w = h[c.displayValue];
					if (!n && c.highlightMatches && d !== "") {
						var v = d,
						x = w.toLowerCase().indexOf(d.toLowerCase()),
						x = '<span class="' + c.matchClass + '">' + w.substr(x, d.length) + "</span>";
						p.match("<(.|\n)*?>") && (m = true, v = "(>)([^<]*?)(" + d + ")((.|\n)*?)(<)", x = '$1$2<span class="' + c.matchClass + '">$3</span>$4$6');
						p = p.replace(RegExp(v, c.highlightMatchesRegExModifier), x)
					}
					c.autoCompleteFirstMatch && ! m && j === 0 && d.length > 0 && w.toLowerCase().indexOf(d.toLowerCase()) === 0 && (G.attr("pq", d), G.val(w), o = t(d.length, G.val().length));
					if (!c.showResults) return;
					$row = a("<div></div>").attr("id", h[c.displayValue]).attr("val", h[c.hiddenValue]).addClass("row").html(p).appendTo(L);
					(n || ++f == 1 && c.selectFirstMatch || o) && $row.addClass(c.selectClass);
					g += p.length
				}
				if (g === 0) q();
				else return P.parent().css("z-index", 11E3),
				P.show(),
				L.children("div").mouseover(function() {
					L.children("div").removeClass(c.selectClass);
					a(this).addClass(c.selectClass)
				}).mouseup(function(a) {
					a.preventDefault();
					a.stopPropagation();
					aa()
				}),
				c.maxVisibleRows > 0 && (f = $row.outerHeight() * c.maxVisibleRows, L.css("max-height", f)),
				g
			}
		}
		function t(a, b) {
			var c = G[0];
			if (c.createTextRange) {
				var d = c.createTextRange();
				d.moveStart("character", a);
				d.moveEnd("character", b - c.value.length);
				d.select()
			} else c.setSelectionRange && c.setSelectionRange(a, b);
			c.focus();
			return true
		}
		function q() {
			G.data("active", false);
			ha.css("z-index", 0);
			P.hide()
		}
		function w() {
			if (!P.is(":visible")) return false;
			var a = L.children("div." + c.selectClass);
			a.length || (a = false);
			return a
		}
		function aa() {
			if ($curr = w()) G.val($curr.attr("id")).focus(),
			gb.val($curr.attr("val")),
			q(),
			c.onSelect && (G.attr("hiddenValue", gb.val()), c.onSelect.apply(G[0]))
		}
		function F() {
			try {
				return document.getBoxObjectFor(document.body),
				true
			} catch(a) {
				return false
			}
		}
		function Ma() {
			try {
				return document.body.getBoundingClientRect(),
				true
			} catch(a) {
				return false
			}
		}
		var M = false,
		Q = [],
		A = [],
		v = 0,
		N = "\u25ca",
		x = c.paging && c.paging.pageSize ? c.paging.pageSize: 0,
		ha = a(b).css("position", "relative").css("z-index", 0),
		gb = a('<input type="hidden"/>').attr("id", ha.attr("id") + "_hidden").attr("name", ha.attr("id")).val(c.initialValue).appendTo(ha),
		G = a("<input/>").attr("id", ha.attr("id") + "_input").attr("autocomplete", "off").addClass(c.inputClass).css("width", c.width + "px").appendTo(ha).click(function() {
			c.watermark !== "" && this.value === c.watermark ? this.value = "": this.select()
		}).focus(function() {
			a(this).removeClass("watermark")
		}).blur(function() {
			setTimeout(function() {
				G.data("active") || q()
			},
			200)
		}).keydown(function(b) {
			var g = 0;
			typeof b.ctrlKey !== "undefined" ? (b.ctrlKey && (g |= 1), b.shiftKey && (g |= 2)) : (b.modifiers & Event.CONTROL_MASK && (g |= 1), b.modifiers & Event.SHIFT_MASK && (g |= 2));
			if (!/16$|17$/.test(b.keyCode)) {
				var f = b.keyCode === 9,
				j = b.keyCode === 27,
				g = b.keyCode === 9 && g > 0,
				h = b.keyCode === 8;
				f && w() && aa();
				if (/27$|38$|33$|34$/.test(b.keyCode) && P.is(":visible") || /13$|40$/.test(b.keyCode) || ! c.allowInput) switch (b.preventDefault && b.preventDefault(), b.stopPropagation && b.stopPropagation(), b.cancelBubble = true, b.returnValue = false, b.keyCode) {
				case 38:
					if (($curr = w()) && $curr.prev().length > 0) {
						$curr.removeClass(c.selectClass).prev().addClass(c.selectClass);
						var p = L.attr("scrollTop"),
						n = $curr[0],
						o = $curr.parent()[0],
						m,
						t,
						v;
						if (F()) v = document.getBoxObjectFor(n).height,
						m = document.getBoxObjectFor(L[0]).y - v * 2,
						t = document.getBoxObjectFor(n).y - document.getBoxObjectFor(L[0]).y;
						else if (Ma()) m = o.getBoundingClientRect().top,
						v = n.getBoundingClientRect(),
						t = v.top,
						v = v.bottom - t;
						t <= m && L.attr("scrollTop", p - v)
					} else $curr || L.children("div:last-child").addClass(c.selectClass);
					break;
				case 40:
					if (P.is(":visible")) if (($curr = w()) && $curr.next().length > 0) {
						$curr.removeClass(c.selectClass).next().addClass(c.selectClass);
						m = L.attr("scrollTop");
						t = $curr[0];
						if (F()) p = document.getBoxObjectFor(L[0]).y + L.attr("offsetHeight"),
						n = document.getBoxObjectFor(t).y + $curr.attr("offsetHeight"),
						o = document.getBoxObjectFor(t).height;
						else if (Ma()) p = L[0].getBoundingClientRect().bottom,
						t = t.getBoundingClientRect(),
						n = t.bottom,
						o = n - t.top;
						n >= p && L.attr("scrollTop", m + o)
					} else $curr || L.children("div:first-child").addClass(c.selectClass);
					else d(true);
					break;
				case 13:
					w() ? aa() : d(true);
					break;
				case 27:
					q();
					break;
				case 34:
					if (c.paging) a("#" + ha.attr("id") + "n").click();
					else if (($curr = w()) && $curr.next().length > 0) {
						$curr.removeClass(c.selectClass);
						for (m = 0; m < c.maxVisibleRows; m++) $curr.next().length > 0 && ($curr = $curr.next());
						$curr.addClass(c.selectClass);
						m = L.attr("scrollTop");
						L.attr("scrollTop", m + L.height())
					} else $curr || L.children("div:first-child").addClass(c.selectClass);
					break;
				case 33:
					if (c.paging) a("#" + ha.attr("id") + "p").click();
					else if (($curr = w()) && $curr.prev().length > 0) {
						$curr.removeClass(c.selectClass);
						for (m = 0; m < c.maxVisibleRows; m++) $curr.prev().length > 0 && ($curr = $curr.prev());
						$curr.addClass(c.selectClass);
						m = L.attr("scrollTop");
						L.attr("scrollTop", m - L.height())
					} else $curr || L.children("div:last-child").addClass(c.selectClass)
				} else ! j && ! f && ! g && d(false, h)
			}
		});
		c.initialValue !== "" ? G.val(c.initialValue).removeClass("watermark") : G.val(c.watermark).addClass("watermark");
		var Da = 0;
		if (c.showArrow && c.showResults) {
			var Y = function() {
				P.is(":visible") ? q() : (G.focus(), c.watermark !== "" && G.val() === c.watermark ? G.val("") : G.select(), M && clearTimeout(M), M = setTimeout(function() {
					f(1, true, c.arrowQuery)
				},
				c.queryDelay))
			},
			Da = a("<span></span>").attr("id", ha.attr("id") + "_arrow").addClass(c.arrowClass).addClass("out").hover(function() {
				a(this).removeClass("out").addClass("over")
			},
			function() {
				a(this).removeClass("over").addClass("out")
			}).mousedown(function() {
				a(this).removeClass("over").addClass("active")
			}).mouseup(function() {
				a(this).removeClass("active").addClass("over")
			}).click(Y).appendTo(ha).width();
			G.css("width", c.width - Da + "px")
		}
		if (!c.allowInput) c.selectFirstMatch = false,
		G.click(Y);
		var Y = G.outerHeight() - G.height() - 2,
		Z = G.outerWidth() - 2,
		da = G.outerHeight();
		Y === 0 ? (Z += 4, da += 4) : Y !== 4 && (Z += Y, da += Y);
		var P = a("<div></div>").attr("id", ha.attr("id") + "_ctr").css("width", Z + Da).css("top", da).css("left", 0).addClass(c.containerClass).appendTo(ha).mousedown(function() {
			G.data("active", true)
		}).hide(),
		L = a("<div></div>").addClass(c.contentClass).appendTo(P).scroll(function() {}),
		U = a("<div></div>").appendTo(P);
		ha.css("height", G.outerHeight());
		String.prototype.applyTemplate = function(a) {
			try {
				return a === "" ? this: this.replace(/{([^{}]*)}/g, function(b, c) {
					var d;
					if (c.indexOf(".") !== - 1) {
						d = c.split(".");
						for (var g = a, f = 0; f < d.length; f++) g = g[d[f]];
						d = g
					} else d = a[c];
					if (typeof d === "string" || typeof d === "number") return d;
					else throw b;
				})
			} catch(b) {
				alert("Invalid JSON property " + b + " found when trying to apply resultTemplate or paging.summaryTemplate.\nPlease check your spelling and try again.")
			}
		}
	};
	a.fn.flexbox = function(b, c) {
		if (b) try {
			var d = a.fn.flexbox.defaults,
			f = a.extend({},
			d, c),
			h;
			for (h in f) if (d[h] === void 0) throw "Invalid option specified: " + h + "\nPlease check your spelling and try again.";
			f.source = b;
			if (c) {
				f.paging = c.paging || c.paging == null ? a.extend({},
				d.paging, c.paging) : false;
				for (h in f.paging) if (d.paging[h] === void 0) throw "Invalid option specified: " + h + "\nPlease check your spelling and try again.";
				if (c.displayValue && ! c.hiddenValue) f.hiddenValue = c.displayValue
			}
			this.each(function() {
				new a.flexbox(this, f)
			});
			return this
		} catch(n) {
			typeof n === "object" ? alert(n.message) : alert(n)
		}
	};
	a.fn.flexbox.defaults = {
		method: "GET",
		queryDelay: 100,
		allowInput: true,
		containerClass: "ffb",
		contentClass: "content",
		selectClass: "ffb-sel",
		inputClass: "ffb-input",
		arrowClass: "ffb-arrow",
		matchClass: "ffb-match",
		noResultsText: "No matching results",
		noResultsClass: "ffb-no-results",
		showResults: true,
		selectFirstMatch: true,
		autoCompleteFirstMatch: false,
		highlightMatches: true,
		highlightMatchesRegExModifier: "i",
		minChars: 1,
		showArrow: true,
		arrowQuery: "",
		onSelect: false,
		maxCacheBytes: 32768,
		resultTemplate: "{name}",
		displayValue: "name",
		hiddenValue: "id",
		initialValue: "",
		watermark: "",
		width: 200,
		resultsProperty: "results",
		totalProperty: "total",
		maxVisibleRows: 0,
		paging: {
			style: "input",
			cssClass: "paging",
			pageSize: 10,
			maxPageLinks: 5,
			showSummary: true,
			summaryClass: "summary",
			summaryTemplate: "Displaying {start}-{end} of {total} results"
		}
	};
	a.fn.setValue = function(b) {
		var c = "#" + this.attr("id");
		a(c + "_hidden," + c + "_input").val(b).removeClass("watermark")
	}
})(jQuery);
$.fx.speeds._default = 500;
$(function() {
	$("#open-chat").click(function() {
		$("#chat-frame").css("display") == "none" ? ($("#chat-frame").fadeIn(300), $("#chat-icon").attr("src", "/static/icons/chat.gif")) : $("#chat-frame").fadeOut(300);
		return false
	});
	$("#chat-close").click(function() {
		$("#chat-frame").fadeOut(300)
	})
});
var chat = {
	stringify: function(a) {
		var b = typeof a;
		if (b != "object" || a === null) return b == "string" && (a = '"' + a + '"'),
		String(a);
		else {
			var c, d, f = [],
			h = a && a.constructor == Array;
			for (c in a) d = a[c],
			b = typeof d,
			b == "string" ? d = '"' + d + '"': b == "object" && d !== null && (d = JSON.stringify(d)),
			f.push((h ? "": '"' + c + '":') + String(d));
			return (h ? "[": "{") + String(f) + (h ? "]": "}")
		}
	},
	linsearch: function(a, b) {
		k = false;
		for (var c = 0; c <= a.length - 1; c++) if (a[c] == b) {
			k = true;
			break
		}
		return k
	},
	check_userslist: function(a, b) {
		k = true;
		for (var c = 0; c <= b.length - 1; c++) if (chat.linsearch(a, b[c]) == false) {
			k = false;
			break
		}
		for (c = 0; c <= a.length - 1; c++) if (chat.linsearch(b, a[c]) == false) {
			k = false;
			break
		}
		return k
	},
	check_conferenceslist: function(a, b) {
		for (var c = 0; c <= b.length - 1; c++) if (chat.linsearch(a, b[c]) == false) chat.ui.on_close_conference(b[c])
	},
	parse_json_conference: function(a) {
		chat.events.on_conferences_list(a.conferences);
		chat.events.on_users_list(a.users);
		chat.events.on_messages(a.new_data);
		if (a.notifications) a.notifications.length = a.notifications.length || [],
		a.notifications.length > 0 && treeio.process_notifications(a.notifications)
	},
	get_location: function() {
		return window.location.hash == "" ? "#": "" + window.location.hash
	},
	sendJSON: function(a) {
		a.location = chat.get_location();
		data = chat.stringify(a);
		$.ajax({
			type: "POST",
			url: chat.option.url,
			typedata: "json",
			data: {
				json: data
			},
			timeout: chat.option.timeout,
			success: function(a) {
				chat.parse_json_conference(a)
			}
		})
	},
	connect: function() {
		chat.sendJSON({
			cmd: "Connect"
		});
		chat.events.on_connect()
	},
	disconnect: function() {
		sendJSON({
			cmd: "Disconnect"
		});
		chat.events.on_disconnect()
	},
	send: function(a, b) {
		json = {
			cmd: "Message",
			data: {
				id: a,
				text: b
			}
		};
		chat.sendJSON(json)
	},
	exit_from_conference: function(a) {
		json = {
			cmd: "Exit",
			data: {
				id: a
			}
		};
		chat.sendJSON(json)
	},
	get_new_messages: function() {
		json = {
			cmd: "Get",
			location: chat.get_location()
		};
		data = chat.stringify(json);
		$.ajax({
			type: "POST",
			url: chat.option.url,
			typedata: "json",
			data: {
				json: data
			},
			timeout: chat.option.timeout,
			success: function(a) {
				chat.parse_json_conference(a)
			},
			complete: function() {
				setTimeout(chat.get_new_messages, chat.option.interval)
			}
		})
	},
	delete_conference: function(a) {
		json = {
			cmd: "Delete",
			data: {
				id: a
			}
		};
		chat.sendJSON(json)
	},
	remove_users_in_conference: function(a, b) {
		json = {
			cmd: "Remove",
			data: {
				id: a,
				users: b
			}
		};
		chat.sendJSON(json)
	},
	add_users_in_conference: function(a, b) {
		json = {
			cmd: "Add",
			data: {
				id: a,
				users: b
			}
		};
		chat.sendJSON(json)
	},
	create_conference: function(a, b) {
		json = {
			cmd: "Create",
			data: {
				title: a,
				users: b
			}
		};
		chat.sendJSON(json)
	}
};
chat.events = {
	on_connect: function() {
		chat.get_new_messages()
	},
	on_disconnect: function() {},
	on_messages: function() {},
	on_users_list: function() {},
	on_conferences_list: function() {}
};
chat.option = {
	interval: 25E3,
	url: "/chat",
	timeout: 6E4
};
chat.ui = {
	add_nick_in_input: function(a) {
		$("#chat-input-msg").val($("#chat-input-msg").val() + a + ": ");
		$("#chat-input-msg").focus()
	},
	get_id_active_conference: function() {
		activeTab = $("#chat-tabs").tabs("option", "selected");
		id_conference = $($(".ui-tabs-panel").get()[activeTab]).attr("id");
		return "" + id_conference
	},
	send_msg: function() {
		chat.send(chat.ui.get_id_active_conference(), $("#chat-input-msg").val());
		$("#chat-input-msg").val("")
	},
	get_json_userlist: function() {
		data = {
			results: []
		};
		$.each($(".chat-users p"), function() {
			$(this).text() != "+" && data.results.push({
				id: $(this).attr("user"),
				name: $(this).text()
			})
		});
		return data
	},
	on_close_conference: function(a) {
		$("li a[href=#" + a + "]").prev("img").attr("src", "/static/icons/forest.png");
		delete chat.conferences_dic[a]
	}
};
chat.conferences_dic = {};
chat.userslist = {
	results: [],
	users: []
};
chat.events.on_users_list = function(a) {
	a = a || [];
	users_list = function() {
		list = [];
		if (a) for (var b = 0; b < a.length; b++) list.push(a[b].name);
		return list
	} ();
	$("#chat-title").text("Chat (" + a.length + ")");
	if (a.length > 0) if (chat.check_userslist(chat.userslist.users, users_list) == false) {
		$(".chat-users").html("");
		for (var b = 0; b < a.length; b++) $("<div/>").append($("<p/>", {
			text: a[b].profile,
			user: a[b].name
		}).bind("dblclick", function() {
			chat.create_conference($(this).text().split(" ", 1), [$(this).attr("user")])
		})).append($("<span/>").addClass("chat-users-actions").append($("<a/>", {
			text: "+",
			user: a[b].name
		}).addClass("chat-invite-user").bind("click", function() {
			chat.add_users_in_conference(chat.ui.get_id_active_conference(), [$(this).attr("user")]);
			$("a.chat-invite-user").hide();
			$("div.chat-fb-div").hide()
		})).append(' <a href="' + a[b].location + '">#</a>')).append($("<br/>")).appendTo(".chat-users");
		a.length == 0 && $(".chat-users").html("<p>No users online</p>");
		chat.userslist.results = chat.ui.get_json_userlist().results;
		$(".chat-fb").html("");
		$(".chat-fb").flexbox(chat.ui.get_json_userlist(), {
			width: 100,
			maxVisibleRows: 10,
			onSelect: function() {
				chat.add_users_in_conference(chat.ui.get_id_active_conference(), [$(this).attr("hiddenvalue")])
			}
		})
	} else for (b = 0; b < a.length; b++) $("a[user='" + a[b].name + "'] + a").attr("href", a[b].location);
	else $(".chat-users").html(""),
	$(".chat-users").append($("<p/>", {
		text: "No users online"
	}));
	chat.userslist.users = users_list
};
chat.events.on_conferences_list = function(a) {
	function b(a) {
		list = [];
		a = a || [];
		if (a.length > 0) for (var b = 0; b < a.length; b++) list.push(a[b].username);
		return list
	}
	function c() {
		$("<p/>").text("Between you,").appendTo("#" + conference.id + " .chat-with");
		for (var a = 0; a < conference.users.length; a++) user = conference.users[a],
		$("<p/>").text(user.profile.split(" ", 1)[0]).appendTo("#" + conference.id + " .chat-with");
		$("<p/>").append($("<a/>", {
			text: "Invite more people"
		}).attr("class", "chat-invite").bind("click", function() {
			$("#" + chat.ui.get_id_active_conference() + " .chat-fb-div").toggle();
			$("a.chat-invite-user").toggle();
			$("#" + chat.ui.get_id_active_conference() + " .chat-fb #_input").focus()
		})).appendTo("#" + conference.id + " .chat-with");
		conference.users.length == 2 && $("a[href='#" + conference.id + "']").text(conference.users[0].profile.split(" ", 1)[0] + " and " + conference.users[1].profile.split(" ", 1)[0]);
		conference.users.length > 2 && $("a[href='#" + conference.id + "']").text(conference.users[0].profile.split(" ", 1)[0] + ", " + conference.users[1].profile.split(" ", 1)[0] + ", ...")
	}
	a = a || [];
	my_list_conferences = [];
	list_conferences = function(a) {
		list = [];
		a = a || [];
		if (a.length > 0) for (var b = 0; b < a.length; b++) list.push(a[b].id);
		return list
	} (a);
	for (var d in chat.conferences_dic) my_list_conferences.push(d);
	chat.check_conferenceslist(list_conferences, my_list_conferences);
	if (a.length > 0) for (d = 0; d < a.length; d++) conference = a[d],
	id = conference.id,
	list_users = b(conference.users),
	chat.conferences_dic[id] ? chat.check_userslist(chat.conferences_dic[conference.id].users, list_users) == false && ($("#" + conference.id + " .chat-with").html(""), c()) : ($("#chat-tabs").tabs("add", "#" + conference.id, conference.title), chat.conferences_dic[id] = {},
	chat.conferences_dic[id].active = true, chat.conferences_dic[id].users = [], $("<div/>").attr("class", "chat-with small").appendTo("#" + conference.id), $("<div/>").attr("class", "chat-fb-div").append($("<div/>").attr("class", "chat-fb").flexbox(chat.userslist, {
		width: 100,
		maxVisibleRows: 10,
		onSelect: function() {
			chat.add_users_in_conference(chat.ui.get_id_active_conference(), [$(this).attr("hiddenvalue")])
		}
	})).append($("<div/>").attr("class", "ui-icon ui-icon-close vertical").bind("click", function() {
		$(this).parent().hide();
		$("a.chat-invite-user").hide()
	})).appendTo("#" + conference.id), $("<div/>").attr("class", "chat-body").appendTo("#" + conference.id), c()),
	chat.conferences_dic[conference.id].users = b(conference.users)
};
chat.events.on_messages = function(a) {
	a = a || [];
	if (a.length > 0) {
		for (var b = 0; b < a.length; b++) {
			new_msg = a[b];
			for (var c in new_msg) {
				msg = new_msg[c].messages;
				for (var d = 0; d < msg.length; d++) text = msg[d].text,
				date = msg[d].date,
				time = msg[d].time,
				user = msg[d].user,
				profile = msg[d].profile,
				$("<div/>").attr("class", "message").append($("<div/>", {
					text: "[" + time + "]"
				}).attr("class", "time")).append($("<div/>", {
					user: user,
					text: "<" + profile + "> "
				}).attr("class", "nick").bind("click", function() {
					chat.ui.add_nick_in_input($(this).text().slice(1, - 2))
				})).append($("<div/>", {
					text: " " + text
				}).attr("class", "text")).appendTo("#" + c + " .chat-body");
				msg.length > 0 && $("li a[href=#" + c + "]").prev("img").fadeIn(100).fadeOut(100).fadeIn(100).fadeOut(100).fadeIn(100).fadeOut(100).fadeIn(100);
				$("#" + c + " .chat-body").animate({
					scrollTop: $("#" + c + " .chat-body").attr("scrollHeight")
				},
				1E3)
			}
		}
		$("#chat-frame").css("display") == "none" && $("#chat-icon").attr("src", "/static/icons/chat-active.gif").fadeOut(100).fadeIn(100).fadeOut(100).fadeIn(100).fadeOut(100).fadeIn(100)
	}
};
/*$(function() {
	$("#chat-tabs").tabs({
		tabTemplate: "<li><img src='/static/icons/forest-active.png' class='margin-bottom' style='float: left;'><a href='#{href}'>#{label}</a><span class='ui-icon ui-icon-close'>Remove Tab</span></li>"
	});
	$("#chat-tabs li span.ui-icon-close").live("click", function() {
		delete chat.conferences_dic[chat.ui.get_id_active_conference()];
		chat.exit_from_conference(chat.ui.get_id_active_conference());
		var a = $("li", $("#chat-tabs")).index($(this).parent());
		$("#chat-tabs").tabs("remove", a)
	});
	$("#chat-input-msg").keypress(function(a) {
		if (a.which == "13") return chat.ui.send_msg(),
		false
	});
	$("#chat-btn-send").click(chat.ui.send_msg);
	chat.connect();
	$(".chat-fb").flexbox(chat.ui.get_json_userlist(), {
		width: 100,
		maxVisibleRows: 10,
		onSelect: function() {
			chat.add_users_in_conference(chat.ui.get_id_active_conference(), [$(this).attr("hiddenvalue")])
		}
	})
});
$(function() {
	var a = $("#tab_title"),
	b = $("#chat-dialog").dialog({
		autoOpen: false,
		modal: true,
		buttons: {
			Invite: function() {
				users = [];
				$.each($(".chat-dialog-users input:checked"), function() {
					users.push($(this).attr("name"))
				});
				users.length > 0 && chat.add_users_in_conference(chat.ui.get_id_active_conference(), users);
				$(this).dialog("close")
			},
			Cancel: function() {
				$(this).dialog("close")
			}
		},
		open: function() {
			$(".chat-dialog-users").html("");
			$.each($(".chat-users p"), function() {
				$("<input>", {
					name: $(this).attr("user"),
					type: "CHECKBOX"
				}).appendTo($(".chat-dialog-users"));
				$(".chat-dialog-users").append($(this).text()).append($("<br/>"))
			});
			a.focus()
		},
		close: function() {
			c[0].reset()
		}
	}),
	c = $("form", b).submit(function() {
		b.dialog("close");
		return false
	})
});*/
Date.CultureInfo = {
	name: "en-US",
	englishName: "English (United States)",
	nativeName: "English (United States)",
	dayNames: "Sunday,Monday,Tuesday,Wednesday,Thursday,Friday,Saturday".split(","),
	abbreviatedDayNames: "Sun,Mon,Tue,Wed,Thu,Fri,Sat".split(","),
	shortestDayNames: "Su,Mo,Tu,We,Th,Fr,Sa".split(","),
	firstLetterDayNames: "S,M,T,W,T,F,S".split(","),
	monthNames: "January,February,March,April,May,June,July,August,September,October,November,December".split(","),
	abbreviatedMonthNames: "Jan,Feb,Mar,Apr,May,Jun,Jul,Aug,Sep,Oct,Nov,Dec".split(","),
	amDesignator: "AM",
	pmDesignator: "PM",
	firstDayOfWeek: 0,
	twoDigitYearMax: 2029,
	dateElementOrder: "mdy",
	formatPatterns: {
		shortDate: "M/d/yyyy",
		longDate: "dddd, MMMM dd, yyyy",
		shortTime: "h:mm tt",
		longTime: "h:mm:ss tt",
		fullDateTime: "dddd, MMMM dd, yyyy h:mm:ss tt",
		sortableDateTime: "yyyy-MM-ddTHH:mm:ss",
		universalSortableDateTime: "yyyy-MM-dd HH:mm:ssZ",
		rfc1123: "ddd, dd MMM yyyy HH:mm:ss GMT",
		monthDay: "MMMM dd",
		yearMonth: "MMMM, yyyy"
	},
	regexPatterns: {
		jan: /^jan(uary)?/i,
		feb: /^feb(ruary)?/i,
		mar: /^mar(ch)?/i,
		apr: /^apr(il)?/i,
		may: /^may/i,
		jun: /^jun(e)?/i,
		jul: /^jul(y)?/i,
		aug: /^aug(ust)?/i,
		sep: /^sep(t(ember)?)?/i,
		oct: /^oct(ober)?/i,
		nov: /^nov(ember)?/i,
		dec: /^dec(ember)?/i,
		sun: /^su(n(day)?)?/i,
		mon: /^mo(n(day)?)?/i,
		tue: /^tu(e(s(day)?)?)?/i,
		wed: /^we(d(nesday)?)?/i,
		thu: /^th(u(r(s(day)?)?)?)?/i,
		fri: /^fr(i(day)?)?/i,
		sat: /^sa(t(urday)?)?/i,
		future: /^next/i,
		past: /^last|past|prev(ious)?/i,
		add: /^(\+|aft(er)?|from|hence)/i,
		subtract: /^(\-|bef(ore)?|ago)/i,
		yesterday: /^yes(terday)?/i,
		today: /^t(od(ay)?)?/i,
		tomorrow: /^tom(orrow)?/i,
		now: /^n(ow)?/i,
		millisecond: /^ms|milli(second)?s?/i,
		second: /^sec(ond)?s?/i,
		minute: /^mn|min(ute)?s?/i,
		hour: /^h(our)?s?/i,
		week: /^w(eek)?s?/i,
		month: /^m(onth)?s?/i,
		day: /^d(ay)?s?/i,
		year: /^y(ear)?s?/i,
		shortMeridian: /^(a|p)/i,
		longMeridian: /^(a\.?m?\.?|p\.?m?\.?)/i,
		timezone: /^((e(s|d)t|c(s|d)t|m(s|d)t|p(s|d)t)|((gmt)?\s*(\+|\-)\s*\d\d\d\d?)|gmt|utc)/i,
		ordinalSuffix: /^\s*(st|nd|rd|th)/i,
		timeContext: /^\s*(\:|a(?!u|p)|p)/i
	},
	timezones: [{
		name: "UTC",
		offset: "-000"
	},
	{
		name: "GMT",
		offset: "-000"
	},
	{
		name: "EST",
		offset: "-0500"
	},
	{
		name: "EDT",
		offset: "-0400"
	},
	{
		name: "CST",
		offset: "-0600"
	},
	{
		name: "CDT",
		offset: "-0500"
	},
	{
		name: "MST",
		offset: "-0700"
	},
	{
		name: "MDT",
		offset: "-0600"
	},
	{
		name: "PST",
		offset: "-0800"
	},
	{
		name: "PDT",
		offset: "-0700"
	}]
};
(function() {
	var a = Date,
	b = a.prototype,
	c = a.CultureInfo,
	d = function(a, b) {
		b || (b = 2);
		return ("000" + a).slice(b * - 1)
	};
	b.clearTime = function() {
		this.setHours(0);
		this.setMinutes(0);
		this.setSeconds(0);
		this.setMilliseconds(0);
		return this
	};
	b.setTimeToNow = function() {
		var a = new Date;
		this.setHours(a.getHours());
		this.setMinutes(a.getMinutes());
		this.setSeconds(a.getSeconds());
		this.setMilliseconds(a.getMilliseconds());
		return this
	};
	a.today = function() {
		return (new Date).clearTime()
	};
	a.compare = function(a, b) {
		if (isNaN(a) || isNaN(b)) throw Error(a + " - " + b);
		else if (a instanceof Date && b instanceof Date) return a < b ? - 1: a > b ? 1: 0;
		else throw new TypeError(a + " - " + b);
	};
	a.equals = function(a, b) {
		return a.compareTo(b) === 0
	};
	a.getDayNumberFromName = function(a) {
		for (var b = c.dayNames, d = c.abbreviatedDayNames, f = c.shortestDayNames, a = a.toLowerCase(), h = 0; h < b.length; h++) if (b[h].toLowerCase() == a || d[h].toLowerCase() == a || f[h].toLowerCase() == a) return h;
		return - 1
	};
	a.getMonthNumberFromName = function(a) {
		for (var b = c.monthNames, d = c.abbreviatedMonthNames, a = a.toLowerCase(), f = 0; f < b.length; f++) if (b[f].toLowerCase() == a || d[f].toLowerCase() == a) return f;
		return - 1
	};
	a.isLeapYear = function(a) {
		return a % 4 === 0 && a % 100 !== 0 || a % 400 === 0
	};
	a.getDaysInMonth = function(b, c) {
		return [31, a.isLeapYear(b) ? 29: 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31][c]
	};
	a.getTimezoneAbbreviation = function(a) {
		for (var b = c.timezones, d = 0; d < b.length; d++) if (b[d].offset === a) return b[d].name;
		return null
	};
	a.getTimezoneOffset = function(a) {
		for (var b = c.timezones, d = 0; d < b.length; d++) if (b[d].name === a.toUpperCase()) return b[d].offset;
		return null
	};
	b.clone = function() {
		return new Date(this.getTime())
	};
	b.compareTo = function(a) {
		return Date.compare(this, a)
	};
	b.equals = function(a) {
		return Date.equals(this, a || new Date)
	};
	b.between = function(a, b) {
		return this.getTime() >= a.getTime() && this.getTime() <= b.getTime()
	};
	b.isAfter = function(a) {
		return this.compareTo(a || new Date) === 1
	};
	b.isBefore = function(a) {
		return this.compareTo(a || new Date) === - 1
	};
	b.isToday = function() {
		return this.isSameDay(new Date)
	};
	b.isSameDay = function(a) {
		return this.clone().clearTime().equals(a.clone().clearTime())
	};
	b.addMilliseconds = function(a) {
		this.setMilliseconds(this.getMilliseconds() + a);
		return this
	};
	b.addSeconds = function(a) {
		return this.addMilliseconds(a * 1E3)
	};
	b.addMinutes = function(a) {
		return this.addMilliseconds(a * 6E4)
	};
	b.addHours = function(a) {
		return this.addMilliseconds(a * 36E5)
	};
	b.addDays = function(a) {
		this.setDate(this.getDate() + a);
		return this
	};
	b.addWeeks = function(a) {
		return this.addDays(a * 7)
	};
	b.addMonths = function(b) {
		var c = this.getDate();
		this.setDate(1);
		this.setMonth(this.getMonth() + b);
		this.setDate(Math.min(c, a.getDaysInMonth(this.getFullYear(), this.getMonth())));
		return this
	};
	b.addYears = function(a) {
		return this.addMonths(a * 12)
	};
	b.add = function(a) {
		if (typeof a == "number") return this._orient = a,
		this;
		a.milliseconds && this.addMilliseconds(a.milliseconds);
		a.seconds && this.addSeconds(a.seconds);
		a.minutes && this.addMinutes(a.minutes);
		a.hours && this.addHours(a.hours);
		a.weeks && this.addWeeks(a.weeks);
		a.months && this.addMonths(a.months);
		a.years && this.addYears(a.years);
		a.days && this.addDays(a.days);
		return this
	};
	var f, h, n;
	b.getWeek = function() {
		var a, b, c, d, m;
		f = ! f ? this.getFullYear() : f;
		h = ! h ? this.getMonth() + 1: h;
		n = ! n ? this.getDate() : n;
		h <= 2 ? (a = f - 1, b = (a / 4 | 0) - (a / 100 | 0) + (a / 400 | 0), c = b - (((a - 1) / 4 | 0) - ((a - 1) / 100 | 0) + ((a - 1) / 400 | 0)), d = 0, m = n - 1 + 31 * (h - 1)) : (a = f, b = (a / 4 | 0) - (a / 100 | 0) + (a / 400 | 0), c = b - (((a - 1) / 4 | 0) - ((a - 1) / 100 | 0) + ((a - 1) / 400 | 0)), d = c + 1, m = n + (153 * (h - 3) + 2) / 5 + 58 + c);
		a = (a + b) % 7;
		d = m + 3 - (m + a - d) % 7 | 0;
		f = h = n = null;
		return d < 0 ? 53 - ((a - c) / 5 | 0) : d > 364 + c ? 1: (d / 7 | 0) + 1
	};
	b.getISOWeek = function() {
		f = this.getUTCFullYear();
		h = this.getUTCMonth() + 1;
		n = this.getUTCDate();
		return d(this.getWeek())
	};
	b.setWeek = function(a) {
		return this.moveToDayOfWeek(1).addWeeks(a - this.getWeek())
	};
	a._validate = function(a, b, c, d) {
		if (typeof a == "undefined") return false;
		else if (typeof a != "number") throw new TypeError(a + " is not a Number.");
		else if (a < b || a > c) throw new RangeError(a + " is not a valid value for " + d + ".");
		return true
	};
	a.validateMillisecond = function(b) {
		return a._validate(b, 0, 999, "millisecond")
	};
	a.validateSecond = function(b) {
		return a._validate(b, 0, 59, "second")
	};
	a.validateMinute = function(b) {
		return a._validate(b, 0, 59, "minute")
	};
	a.validateHour = function(b) {
		return a._validate(b, 0, 23, "hour")
	};
	a.validateDay = function(b, c, d) {
		return a._validate(b, 1, a.getDaysInMonth(c, d), "day")
	};
	a.validateMonth = function(b) {
		return a._validate(b, 0, 11, "month")
	};
	a.validateYear = function(b) {
		return a._validate(b, 0, 9999, "year")
	};
	b.set = function(b) {
		a.validateMillisecond(b.millisecond) && this.addMilliseconds(b.millisecond - this.getMilliseconds());
		a.validateSecond(b.second) && this.addSeconds(b.second - this.getSeconds());
		a.validateMinute(b.minute) && this.addMinutes(b.minute - this.getMinutes());
		a.validateHour(b.hour) && this.addHours(b.hour - this.getHours());
		a.validateMonth(b.month) && this.addMonths(b.month - this.getMonth());
		a.validateYear(b.year) && this.addYears(b.year - this.getFullYear());
		a.validateDay(b.day, this.getFullYear(), this.getMonth()) && this.addDays(b.day - this.getDate());
		b.timezone && this.setTimezone(b.timezone);
		b.timezoneOffset && this.setTimezoneOffset(b.timezoneOffset);
		b.week && a._validate(b.week, 0, 53, "week") && this.setWeek(b.week);
		return this
	};
	b.moveToFirstDayOfMonth = function() {
		return this.set({
			day: 1
		})
	};
	b.moveToLastDayOfMonth = function() {
		return this.set({
			day: a.getDaysInMonth(this.getFullYear(), this.getMonth())
		})
	};
	b.moveToNthOccurrence = function(a, b) {
		var c = 0;
		if (b > 0) c = b - 1;
		else if (b === - 1) return this.moveToLastDayOfMonth(),
		this.getDay() !== a && this.moveToDayOfWeek(a, - 1),
		this;
		return this.moveToFirstDayOfMonth().addDays( - 1).moveToDayOfWeek(a, 1).addWeeks(c)
	};
	b.moveToDayOfWeek = function(a, b) {
		var c = (a - this.getDay() + 7 * (b || 1)) % 7;
		return this.addDays(c === 0 ? c + 7 * (b || 1) : c)
	};
	b.moveToMonth = function(a, b) {
		var c = (a - this.getMonth() + 12 * (b || 1)) % 12;
		return this.addMonths(c === 0 ? c + 12 * (b || 1) : c)
	};
	b.getOrdinalNumber = function() {
		return Math.ceil((this.clone().clearTime() - new Date(this.getFullYear(), 0, 1)) / 864E5) + 1
	};
	b.getTimezone = function() {
		return a.getTimezoneAbbreviation(this.getUTCOffset())
	};
	b.setTimezoneOffset = function(a) {
		var b = this.getTimezoneOffset();
		return this.addMinutes(Number(a) * - 6 / 10 - b)
	};
	b.setTimezone = function(b) {
		return this.setTimezoneOffset(a.getTimezoneOffset(b))
	};
	b.hasDaylightSavingTime = function() {
		return Date.today().set({
			month: 0,
			day: 1
		}).getTimezoneOffset() !== Date.today().set({
			month: 6,
			day: 1
		}).getTimezoneOffset()
	};
	b.isDaylightSavingTime = function() {
		return this.hasDaylightSavingTime() && (new Date).getTimezoneOffset() === Date.today().set({
			month: 6,
			day: 1
		}).getTimezoneOffset()
	};
	b.getUTCOffset = function() {
		var a = this.getTimezoneOffset() * - 10 / 6;
		return a < 0 ? (a = (a - 1E4).toString(), a.charAt(0) + a.substr(2)) : (a = (a + 1E4).toString(), "+" + a.substr(1))
	};
	b.getElapsed = function(a) {
		return (a || new Date) - this
	};
	if (!b.toISOString) b.toISOString = function() {
		function a(b) {
			return b < 10 ? "0" + b: b
		}
		return '"' + this.getUTCFullYear() + "-" + a(this.getUTCMonth() + 1) + "-" + a(this.getUTCDate()) + "T" + a(this.getUTCHours()) + ":" + a(this.getUTCMinutes()) + ":" + a(this.getUTCSeconds()) + 'Z"'
	};
	b._toString = b.toString;
	b.toString = function(a) {
		var b = this;
		if (a && a.length == 1) {
			var f = c.formatPatterns;
			b.t = b.toString;
			switch (a) {
			case "d":
				return b.t(f.shortDate);
			case "D":
				return b.t(f.longDate);
			case "F":
				return b.t(f.fullDateTime);
			case "m":
				return b.t(f.monthDay);
			case "r":
				return b.t(f.rfc1123);
			case "s":
				return b.t(f.sortableDateTime);
			case "t":
				return b.t(f.shortTime);
			case "T":
				return b.t(f.longTime);
			case "u":
				return b.t(f.universalSortableDateTime);
			case "y":
				return b.t(f.yearMonth)
			}
		}
		var h = function(a) {
			switch (a * 1) {
			case 1:
			case 21:
			case 31:
				return "st";
			case 2:
			case 22:
				return "nd";
			case 3:
			case 23:
				return "rd";
			default:
				return "th"
			}
		};
		return a ? a.replace(/(\\)?(dd?d?d?|MM?M?M?|yy?y?y?|hh?|HH?|mm?|ss?|tt?|S)/g, function(a) {
			if (a.charAt(0) === "\\") return a.replace("\\", "");
			b.h = b.getHours;
			switch (a) {
			case "hh":
				return d(b.h() < 13 ? b.h() === 0 ? 12: b.h() : b.h() - 12);
			case "h":
				return b.h() < 13 ? b.h() === 0 ? 12: b.h() : b.h() - 12;
			case "HH":
				return d(b.h());
			case "H":
				return b.h();
			case "mm":
				return d(b.getMinutes());
			case "m":
				return b.getMinutes();
			case "ss":
				return d(b.getSeconds());
			case "s":
				return b.getSeconds();
			case "yyyy":
				return d(b.getFullYear(), 4);
			case "yy":
				return d(b.getFullYear());
			case "dddd":
				return c.dayNames[b.getDay()];
			case "ddd":
				return c.abbreviatedDayNames[b.getDay()];
			case "dd":
				return d(b.getDate());
			case "d":
				return b.getDate();
			case "MMMM":
				return c.monthNames[b.getMonth()];
			case "MMM":
				return c.abbreviatedMonthNames[b.getMonth()];
			case "MM":
				return d(b.getMonth() + 1);
			case "M":
				return b.getMonth() + 1;
			case "t":
				return b.h() < 12 ? c.amDesignator.substring(0, 1) : c.pmDesignator.substring(0, 1);
			case "tt":
				return b.h() < 12 ? c.amDesignator: c.pmDesignator;
			case "S":
				return h(b.getDate());
			default:
				return a
			}
		}):
		this._toString()
	}
})();
(function() {
	var a = Date,
	b = a.prototype,
	c = a.CultureInfo,
	d = Number.prototype;
	b._orient = 1;
	b._nth = null;
	b._is = false;
	b._same = false;
	b._isSecond = false;
	d._dateElement = "day";
	b.next = function() {
		this._orient = 1;
		return this
	};
	a.next = function() {
		return a.today().next()
	};
	b.last = b.prev = b.previous = function() {
		this._orient = - 1;
		return this
	};
	a.last = a.prev = a.previous = function() {
		return a.today().last()
	};
	b.is = function() {
		this._is = true;
		return this
	};
	b.same = function() {
		this._same = true;
		this._isSecond = false;
		return this
	};
	b.today = function() {
		return this.same().day()
	};
	b.weekday = function() {
		return this._is ? (this._is = false, ! this.is().sat() && ! this.is().sun()) : false
	};
	b.at = function(b) {
		return typeof b === "string" ? a.parse(this.toString("d") + " " + b) : this.set(b)
	};
	d.fromNow = d.after = function(a) {
		var b = {};
		b[this._dateElement] = this;
		return (!a ? new Date: a.clone()).add(b)
	};
	d.ago = d.before = function(a) {
		var b = {};
		b[this._dateElement] = this * - 1;
		return (!a ? new Date: a.clone()).add(b)
	};
	var f = "sunday monday tuesday wednesday thursday friday saturday".split(/\s/),
	h = "january february march april may june july august september october november december".split(/\s/),
	n = "Millisecond Second Minute Hour Day Week Month Year".split(/\s/),
	g = "Milliseconds Seconds Minutes Hours Date Week Month FullYear".split(/\s/),
	p = "final first second third fourth fifth".split(/\s/);
	b.toObject = function() {
		for (var a = {}, b = 0; b < n.length; b++) a[n[b].toLowerCase()] = this["get" + g[b]]();
		return a
	};
	a.fromObject = function(a) {
		a.week = null;
		return Date.today().set(a)
	};
	for (var j = function(b) {
		return function() {
			if (this._is) return this._is = false,
			this.getDay() == b;
			if (this._nth !== null) {
				this._isSecond && this.addSeconds(this._orient * - 1);
				this._isSecond = false;
				var c = this._nth;
				this._nth = null;
				var d = this.clone().moveToLastDayOfMonth();
				this.moveToNthOccurrence(b, c);
				if (this > d) throw new RangeError(a.getDayName(b) + " does not occur " + c + " times in the month of " + a.getMonthName(d.getMonth()) + " " + d.getFullYear() + ".");
				return this
			}
			return this.moveToDayOfWeek(b, this._orient)
		}
	},
	o = function(b) {
		return function() {
			var d = a.today(),
			f = b - d.getDay();
			b === 0 && c.firstDayOfWeek === 1 && d.getDay() !== 0 && (f += 7);
			return d.addDays(f)
		}
	},
	m = 0; m < f.length; m++) a[f[m].toUpperCase()] = a[f[m].toUpperCase().substring(0, 3)] = m,
	a[f[m]] = a[f[m].substring(0, 3)] = o(m),
	b[f[m]] = b[f[m].substring(0, 3)] = j(m);
	f = function(a) {
		return function() {
			return this._is ? (this._is = false, this.getMonth() === a) : this.moveToMonth(a, this._orient)
		}
	};
	j = function(b) {
		return function() {
			return a.today().set({
				month: b,
				day: 1
			})
		}
	};
	for (o = 0; o < h.length; o++) a[h[o].toUpperCase()] = a[h[o].toUpperCase().substring(0, 3)] = o,
	a[h[o]] = a[h[o].substring(0, 3)] = j(o),
	b[h[o]] = b[h[o].substring(0, 3)] = f(o);
	f = function(a) {
		return function(b) {
			if (this._isSecond) return this._isSecond = false,
			this;
			if (this._same) {
				this._same = this._is = false;
				for (var c = this.toObject(), b = (b || new Date).toObject(), d = "", f = a.toLowerCase(), g = n.length - 1; g > - 1; g--) {
					d = n[g].toLowerCase();
					if (c[d] != b[d]) return false;
					if (f == d) break
				}
				return true
			}
			a.substring(a.length - 1) != "s" && (a += "s");
			return this["add" + a](this._orient)
		}
	};
	j = function(a) {
		return function() {
			this._dateElement = a;
			return this
		}
	};
	for (o = 0; o < n.length; o++) h = n[o].toLowerCase(),
	b[h] = b[h + "s"] = f(n[o]),
	d[h] = d[h + "s"] = j(h);
	b._ss = f("Second");
	d = function(a) {
		return function(b) {
			if (this._same) return this._ss(b);
			if (b || b === 0) return this.moveToNthOccurrence(b, a);
			this._nth = a;
			return a === 2 && (b === void 0 || b === null) ? (this._isSecond = true, this.addSeconds(this._orient)) : this
		}
	};
	for (h = 0; h < p.length; h++) b[p[h]] = h === 0 ? d( - 1) : d(h)
})();
(function() {
	Date.Parsing = {
		Exception: function(a) {
			this.message = "Parse error at '" + a.substring(0, 10) + " ...'"
		}
	};
	for (var a = Date.Parsing, b = a.Operators = {
		rtoken: function(b) {
			return function(c) {
				var d = c.match(b);
				if (d) return [d[0], c.substring(d[0].length)];
				else throw new a.Exception(c);
			}
		},
		token: function() {
			return function(a) {
				return b.rtoken(RegExp("^s*" + a + "s*"))(a)
			}
		},
		stoken: function(a) {
			return b.rtoken(RegExp("^" + a))
		},
		until: function(a) {
			return function(b) {
				for (var c = [], d = null; b.length;) {
					try {
						d = a.call(this, b)
					} catch(f) {
						c.push(d[0]);
						b = d[1];
						continue
					}
					break
				}
				return [c, b]
			}
		},
		many: function(a) {
			return function(b) {
				for (var c = [], d = null; b.length;) {
					try {
						d = a.call(this, b)
					} catch(f) {
						break
					}
					c.push(d[0]);
					b = d[1]
				}
				return [c, b]
			}
		},
		optional: function(a) {
			return function(b) {
				var c = null;
				try {
					c = a.call(this, b)
				} catch(d) {
					return [null, b]
				}
				return [c[0], c[1]]
			}
		},
		not: function(b) {
			return function(c) {
				try {
					b.call(this, c)
				} catch(d) {
					return [null, c]
				}
				throw new a.Exception(c);
			}
		},
		ignore: function(a) {
			return a ? function(b) {
				var c = null,
				c = a.call(this, b);
				return [null, c[1]]
			}: null
		},
		product: function() {
			for (var a = arguments[0], c = Array.prototype.slice.call(arguments, 1), d = [], f = 0; f < a.length; f++) d.push(b.each(a[f], c));
			return d
		},
		cache: function(b) {
			var c = {},
			d = null;
			return function(f) {
				try {
					d = c[f] = c[f] || b.call(this, f)
				} catch(j) {
					d = c[f] = j
				}
				if (d instanceof a.Exception) throw d;
				else return d
			}
		},
		any: function() {
			var b = arguments;
			return function(c) {
				for (var d = null, f = 0; f < b.length; f++) if (b[f] != null) {
					try {
						d = b[f].call(this, c)
					} catch(j) {
						d = null
					}
					if (d) return d
				}
				throw new a.Exception(c);
			}
		},
		each: function() {
			var b = arguments;
			return function(c) {
				for (var d = [], f = null, j = 0; j < b.length; j++) if (b[j] != null) {
					try {
						f = b[j].call(this, c)
					} catch(o) {
						throw new a.Exception(c);
					}
					d.push(f[0]);
					c = f[1]
				}
				return [d, c]
			}
		},
		all: function() {
			var a = a;
			return a.each(a.optional(arguments))
		},
		sequence: function(c, d, f) {
			d = d || b.rtoken(/^\s*/);
			f = f || null;
			return c.length == 1 ? c[0] : function(b) {
				for (var j = null, o = null, m = [], t = 0; t < c.length; t++) {
					try {
						j = c[t].call(this, b)
					} catch(q) {
						break
					}
					m.push(j[0]);
					try {
						o = d.call(this, j[1])
					} catch(w) {
						o = null;
						break
					}
					b = o[1]
				}
				if (!j) throw new a.Exception(b);
				if (o) throw new a.Exception(o[1]);
				if (f) try {
					j = f.call(this, j[1])
				} catch(aa) {
					throw new a.Exception(j[1]);
				}
				return [m, j ? j[1] : b]
			}
		},
		between: function(a, c, d) {
			var d = d || a,
			f = b.each(b.ignore(a), c, b.ignore(d));
			return function(a) {
				a = f.call(this, a);
				return [[a[0][0], r[0][2]], a[1]]
			}
		},
		list: function(a, c, d) {
			c = c || b.rtoken(/^\s*/);
			d = d || null;
			return a instanceof Array ? b.each(b.product(a.slice(0, - 1), b.ignore(c)), a.slice( - 1), b.ignore(d)) : b.each(b.many(b.each(a, b.ignore(c))), px, b.ignore(d))
		},
		set: function(c, d, f) {
			d = d || b.rtoken(/^\s*/);
			f = f || null;
			return function(p) {
				for (var j = null, o = null, m = null, t = [[], p], q = false, w = 0; w < c.length; w++) {
					j = o = null;
					q = c.length == 1;
					try {
						j = c[w].call(this, p)
					} catch(aa) {
						continue
					}
					m = [[j[0]], j[1]];
					if (j[1].length > 0 && ! q) try {
						o = d.call(this, j[1])
					} catch(F) {
						q = true
					} else q = true; ! q && o[1].length === 0 && (q = true);
					if (!q) {
						j = [];
						for (q = 0; q < c.length; q++) w != q && j.push(c[q]);
						j = b.set(j, d).call(this, o[1]);
						j[0].length > 0 && (m[0] = m[0].concat(j[0]), m[1] = j[1])
					}
					m[1].length < t[1].length && (t = m);
					if (t[1].length === 0) break
				}
				if (t[0].length === 0) return t;
				if (f) {
					try {
						o = f.call(this, t[1])
					} catch(Ma) {
						throw new a.Exception(t[1]);
					}
					t[1] = o[1]
				}
				return t
			}
		},
		forward: function(a, b) {
			return function(c) {
				return a[b].call(this, c)
			}
		},
		replace: function(a, b) {
			return function(c) {
				c = a.call(this, c);
				return [b, c[1]]
			}
		},
		process: function(a, b) {
			return function(c) {
				c = a.call(this, c);
				return [b.call(this, c[0]), c[1]]
			}
		},
		min: function(b, c) {
			return function(d) {
				var f = c.call(this, d);
				if (f[0].length < b) throw new a.Exception(d);
				return f
			}
		}
	},
	c = function(a) {
		return function() {
			var b = null,
			c = [];
			arguments.length > 1 ? b = Array.prototype.slice.call(arguments) : arguments[0] instanceof Array && (b = arguments[0]);
			if (b) for (var d = b.shift(); 0 < d.length;) return b.unshift(d[0]),
			c.push(a.apply(null, b)),
			b.shift(),
			c;
			else return a.apply(null, arguments)
		}
	},
	d = "optional not ignore cache".split(/\s/), f = 0; f < d.length; f++) b[d[f]] = c(b[d[f]]);
	c = function(a) {
		return function() {
			return arguments[0] instanceof Array ? a.apply(null, arguments[0]) : a.apply(null, arguments)
		}
	};
	d = "each any all".split(/\s/);
	for (f = 0; f < d.length; f++) b[d[f]] = c(b[d[f]])
})();
(function() {
	var a = Date,
	b = a.CultureInfo,
	c = function(a) {
		for (var b = [], d = 0; d < a.length; d++) a[d] instanceof Array ? b = b.concat(c(a[d])) : a[d] && b.push(a[d]);
		return b
	};
	a.Grammar = {};
	a.Translator = {
		hour: function(a) {
			return function() {
				this.hour = Number(a)
			}
		},
		minute: function(a) {
			return function() {
				this.minute = Number(a)
			}
		},
		second: function(a) {
			return function() {
				this.second = Number(a)
			}
		},
		meridian: function(a) {
			return function() {
				this.meridian = a.slice(0, 1).toLowerCase()
			}
		},
		timezone: function(a) {
			return function() {
				var b = a.replace(/[^\d\+\-]/g, "");
				b.length ? this.timezoneOffset = Number(b) : this.timezone = a.toLowerCase()
			}
		},
		day: function(a) {
			var b = a[0];
			return function() {
				this.day = Number(b.match(/\d+/)[0])
			}
		},
		month: function(a) {
			return function() {
				this.month = a.length == 3 ? "jan feb mar apr may jun jul aug sep oct nov dec".indexOf(a) / 4: Number(a) - 1
			}
		},
		year: function(a) {
			return function() {
				var c = Number(a);
				this.year = a.length > 2 ? c: c + (c + 2E3 < b.twoDigitYearMax ? 2E3: 1900)
			}
		},
		rday: function(a) {
			return function() {
				switch (a) {
				case "yesterday":
					this.days = - 1;
					break;
				case "tomorrow":
					this.days = 1;
					break;
				case "today":
					this.days = 0;
					break;
				case "now":
					this.days = 0,
					this.now = true
				}
			}
		},
		finishExact: function(b) {
			for (var b = b instanceof Array ? b: [b], c = 0; c < b.length; c++) b[c] && b[c].call(this);
			b = new Date;
			if ((this.hour || this.minute) && ! this.month && ! this.year && ! this.day) this.day = b.getDate();
			if (!this.year) this.year = b.getFullYear();
			if (!this.month && this.month !== 0) this.month = b.getMonth();
			if (!this.day) this.day = 1;
			if (!this.hour) this.hour = 0;
			if (!this.minute) this.minute = 0;
			if (!this.second) this.second = 0;
			if (this.meridian && this.hour) if (this.meridian == "p" && this.hour < 12) this.hour += 12;
			else if (this.meridian == "a" && this.hour == 12) this.hour = 0;
			if (this.day > a.getDaysInMonth(this.year, this.month)) throw new RangeError(this.day + " is not a valid value for days.");
			b = new Date(this.year, this.month, this.day, this.hour, this.minute, this.second);
			this.timezone ? b.set({
				timezone: this.timezone
			}) : this.timezoneOffset && b.set({
				timezoneOffset: this.timezoneOffset
			});
			return b
		},
		finish: function(b) {
			b = b instanceof Array ? c(b) : [b];
			if (b.length === 0) return null;
			for (var d = 0; d < b.length; d++) typeof b[d] == "function" && b[d].call(this);
			b = a.today();
			if (this.now && ! this.unit && ! this.operator) return new Date;
			else this.now && (b = new Date);
			var d = !! (this.days && this.days !== null || this.orient || this.operator),
			f,
			g,
			h;
			h = this.orient == "past" || this.operator == "subtract" ? - 1: 1; ! this.now && "hour minute second".indexOf(this.unit) != - 1 && b.setTimeToNow();
			if ((this.month || this.month === 0) && "year day hour minute second".indexOf(this.unit) != - 1) this.value = this.month + 1,
			this.month = null,
			d = true;
			if (!d && this.weekday && ! this.day && ! this.days) {
				f = Date[this.weekday]();
				this.day = f.getDate();
				if (!this.month) this.month = f.getMonth();
				this.year = f.getFullYear()
			}
			if (d && this.weekday && this.unit != "month") this.unit = "day",
			f = a.getDayNumberFromName(this.weekday) - b.getDay(),
			g = 7,
			this.days = f ? (f + h * g) % g: h * g;
			if (this.month && this.unit == "day" && this.operator) this.value = this.month + 1,
			this.month = null;
			if (this.value != null && this.month != null && this.year != null) this.day = this.value * 1;
			if (this.month && ! this.day && this.value && (b.set({
				day: this.value * 1
			}), ! d)) this.day = this.value * 1;
			if (!this.month && this.value && this.unit == "month" && ! this.now) this.month = this.value,
			d = true;
			if (d && (this.month || this.month === 0) && this.unit != "year") this.unit = "month",
			f = this.month - b.getMonth(),
			g = 12,
			this.months = f ? (f + h * g) % g: h * g,
			this.month = null;
			if (!this.unit) this.unit = "day";
			if (!this.value && this.operator && this.operator !== null && this[this.unit + "s"] && this[this.unit + "s"] !== null) this[this.unit + "s"] = this[this.unit + "s"] + (this.operator == "add" ? 1: - 1) + (this.value || 0) * h;
			else if (this[this.unit + "s"] == null || this.operator != null) {
				if (!this.value) this.value = 1;
				this[this.unit + "s"] = this.value * h
			}
			if (this.meridian && this.hour) if (this.meridian == "p" && this.hour < 12) this.hour += 12;
			else if (this.meridian == "a" && this.hour == 12) this.hour = 0;
			if (this.weekday && ! this.day && ! this.days && (f = Date[this.weekday](), this.day = f.getDate(), f.getMonth() !== b.getMonth())) this.month = f.getMonth();
			if ((this.month || this.month === 0) && ! this.day) this.day = 1;
			if (!this.orient && ! this.operator && this.unit == "week" && this.value && ! this.day && ! this.month) return Date.today().setWeek(this.value);
			if (d && this.timezone && this.day && this.days) this.day = this.days;
			return d ? b.add(this) : b.set(this)
		}
	};
	var d = a.Parsing.Operators,
	f = a.Grammar,
	h = a.Translator,
	n;
	f.datePartDelimiter = d.rtoken(/^([\s\-\.\,\/\x27]+)/);
	f.timePartDelimiter = d.stoken(":");
	f.whiteSpace = d.rtoken(/^\s*/);
	f.generalDelimiter = d.rtoken(/^(([\s\,]|at|@|on)+)/);
	var g = {};
	f.ctoken = function(a) {
		var c = g[a];
		if (!c) {
			for (var c = b.regexPatterns, f = a.split(/\s+/), h = [], n = 0; n < f.length; n++) h.push(d.replace(d.rtoken(c[f[n]]), f[n]));
			c = g[a] = d.any.apply(null, h)
		}
		return c
	};
	f.ctoken2 = function(a) {
		return d.rtoken(b.regexPatterns[a])
	};
	f.h = d.cache(d.process(d.rtoken(/^(0[0-9]|1[0-2]|[1-9])/), h.hour));
	f.hh = d.cache(d.process(d.rtoken(/^(0[0-9]|1[0-2])/), h.hour));
	f.H = d.cache(d.process(d.rtoken(/^([0-1][0-9]|2[0-3]|[0-9])/), h.hour));
	f.HH = d.cache(d.process(d.rtoken(/^([0-1][0-9]|2[0-3])/), h.hour));
	f.m = d.cache(d.process(d.rtoken(/^([0-5][0-9]|[0-9])/), h.minute));
	f.mm = d.cache(d.process(d.rtoken(/^[0-5][0-9]/), h.minute));
	f.s = d.cache(d.process(d.rtoken(/^([0-5][0-9]|[0-9])/), h.second));
	f.ss = d.cache(d.process(d.rtoken(/^[0-5][0-9]/), h.second));
	f.hms = d.cache(d.sequence([f.H, f.m, f.s], f.timePartDelimiter));
	f.t = d.cache(d.process(f.ctoken2("shortMeridian"), h.meridian));
	f.tt = d.cache(d.process(f.ctoken2("longMeridian"), h.meridian));
	f.z = d.cache(d.process(d.rtoken(/^((\+|\-)\s*\d\d\d\d)|((\+|\-)\d\d\:?\d\d)/), h.timezone));
	f.zz = d.cache(d.process(d.rtoken(/^((\+|\-)\s*\d\d\d\d)|((\+|\-)\d\d\:?\d\d)/), h.timezone));
	f.zzz = d.cache(d.process(f.ctoken2("timezone"), h.timezone));
	f.timeSuffix = d.each(d.ignore(f.whiteSpace), d.set([f.tt, f.zzz]));
	f.time = d.each(d.optional(d.ignore(d.stoken("T"))), f.hms, f.timeSuffix);
	f.d = d.cache(d.process(d.each(d.rtoken(/^([0-2]\d|3[0-1]|\d)/), d.optional(f.ctoken2("ordinalSuffix"))), h.day));
	f.dd = d.cache(d.process(d.each(d.rtoken(/^([0-2]\d|3[0-1])/), d.optional(f.ctoken2("ordinalSuffix"))), h.day));
	f.ddd = f.dddd = d.cache(d.process(f.ctoken("sun mon tue wed thu fri sat"), function(a) {
		return function() {
			this.weekday = a
		}
	}));
	f.M = d.cache(d.process(d.rtoken(/^(1[0-2]|0\d|\d)/), h.month));
	f.MM = d.cache(d.process(d.rtoken(/^(1[0-2]|0\d)/), h.month));
	f.MMM = f.MMMM = d.cache(d.process(f.ctoken("jan feb mar apr may jun jul aug sep oct nov dec"), h.month));
	f.y = d.cache(d.process(d.rtoken(/^(\d\d?)/), h.year));
	f.yy = d.cache(d.process(d.rtoken(/^(\d\d)/), h.year));
	f.yyy = d.cache(d.process(d.rtoken(/^(\d\d?\d?\d?)/), h.year));
	f.yyyy = d.cache(d.process(d.rtoken(/^(\d\d\d\d)/), h.year));
	n = function() {
		return d.each(d.any.apply(null, arguments), d.not(f.ctoken2("timeContext")))
	};
	f.day = n(f.d, f.dd);
	f.month = n(f.M, f.MMM);
	f.year = n(f.yyyy, f.yy);
	f.orientation = d.process(f.ctoken("past future"), function(a) {
		return function() {
			this.orient = a
		}
	});
	f.operator = d.process(f.ctoken("add subtract"), function(a) {
		return function() {
			this.operator = a
		}
	});
	f.rday = d.process(f.ctoken("yesterday tomorrow today now"), h.rday);
	f.unit = d.process(f.ctoken("second minute hour day week month year"), function(a) {
		return function() {
			this.unit = a
		}
	});
	f.value = d.process(d.rtoken(/^\d\d?(st|nd|rd|th)?/), function(a) {
		return function() {
			this.value = a.replace(/\D/g, "")
		}
	});
	f.expression = d.set([f.rday, f.operator, f.value, f.unit, f.orientation, f.ddd, f.MMM]);
	n = function() {
		return d.set(arguments, f.datePartDelimiter)
	};
	f.mdy = n(f.ddd, f.month, f.day, f.year);
	f.ymd = n(f.ddd, f.year, f.month, f.day);
	f.dmy = n(f.ddd, f.day, f.month, f.year);
	f.date = function(a) {
		return (f[b.dateElementOrder] || f.mdy).call(this, a)
	};
	f.format = d.process(d.many(d.any(d.process(d.rtoken(/^(dd?d?d?|MM?M?M?|yy?y?y?|hh?|HH?|mm?|ss?|tt?|zz?z?)/), function(b) {
		if (f[b]) return f[b];
		else throw a.Parsing.Exception(b);
	}), d.process(d.rtoken(/^[^dMyhHmstz]+/), function(a) {
		return d.ignore(d.stoken(a))
	}))), function(a) {
		return d.process(d.each.apply(null, a), h.finishExact)
	});
	var p = {};
	f.formats = function(a) {
		if (a instanceof Array) {
			for (var b = [], c = 0; c < a.length; c++) b.push(p[a[c]] = p[a[c]] || f.format(a[c])[0]);
			return d.any.apply(null, b)
		} else return p[a] = p[a] || f.format(a)[0]
	};
	f._formats = f.formats('"yyyy-MM-ddTHH:mm:ssZ";yyyy-MM-ddTHH:mm:ssZ;yyyy-MM-ddTHH:mm:ssz;yyyy-MM-ddTHH:mm:ss;yyyy-MM-ddTHH:mmZ;yyyy-MM-ddTHH:mmz;yyyy-MM-ddTHH:mm;ddd, MMM dd, yyyy H:mm:ss tt;ddd MMM d yyyy HH:mm:ss zzz;MMddyyyy;ddMMyyyy;Mddyyyy;ddMyyyy;Mdyyyy;dMyyyy;yyyy;Mdyy;dMyy;d'.split(";"));
	f._start = d.process(d.set([f.date, f.time, f.expression], f.generalDelimiter, f.whiteSpace), h.finish);
	f.start = function(a) {
		try {
			var b = f._formats.call({},
			a);
			if (b[1].length === 0) return b
		} catch(c) {}
		return f._start.call({},
		a)
	};
	a._parse = a.parse;
	a.parse = function(b) {
		var c = null;
		if (!b) return null;
		if (b instanceof Date) return b;
		try {
			c = a.Grammar.start.call({},
			b.replace(/^\s*(\S*(\s+\S+)*)\s*$/, "$1"))
		} catch(d) {
			return null
		}
		return c[1].length === 0 ? c[0] : null
	};
	a.getParseFunction = function(b) {
		var c = a.Grammar.formats(b);
		return function(a) {
			var b = null;
			try {
				b = c.call({},
				a)
			} catch(d) {
				return null
			}
			return b[1].length === 0 ? b[0] : null
		}
	};
	a.parseExact = function(b, c) {
		return a.getParseFunction(c)(b)
	}
})();
(function(a) {
	function b(b) {
		function c() {
			var b = h.getBoundaryDatesFromData(j.data, Math.floor(j.slideWidth / j.cellWidth + 5));
			j.start = b[0];
			j.end = b[1];
			p.each(function() {
				var b = a(this),
				c = a("<div>", {
					"class": "ganttview"
				});
				(new d(c, j)).render();
				b.append(c);
				c = a("div.ganttview-vtheader", b).outerWidth() + a("div.ganttview-slide-container", b).outerWidth();
				b.css("width", c + 2 + "px");
				(new f(b, j)).apply()
			})
		}
		var p = this,
		j = a.extend(true, {
			showWeekends: true,
			cellWidth: 21,
			cellHeight: 31,
			slideWidth: 400,
			vHeaderWidth: 100,
			behavior: {
				clickable: true,
				draggable: true,
				resizable: true
			}
		},
		b);
		j.data ? c() : j.dataUrl && a.getJSON(j.dataUrl, function(a) {
			j.data = a;
			c()
		})
	}
	function c(a, c) {
		if (a == "setSlideWidth") {
			var d = $("div.ganttview", this);
			$("div#ganttChart", this);
			d.each(function() {
				var a = $("div.ganttview-vtheader", d).outerWidth();
				$(d).width(c + 1);
				$("div.ganttview-slide-container", this).width(c - a);
				b()
			})
		}
		$("#ganttChart").width(c)
	}
	a.fn.ganttView = function() {
		var a = Array.prototype.slice.call(arguments);
		a.length == 1 && typeof a[0] == "object" && b.call(this, a[0]);
		a.length == 2 && typeof a[0] == "string" && c.call(this, a[0], a[1])
	};
	$(window).resize(function() {
		$("#ganttChart").ganttView("setSlideWidth", $("div.module-block").width() - $("td.module-sidebar").width() - 60)
	});
	var d = function(b, c) {
		function d(b, c, f) {
			c = {
				id: c.id,
				name: c.name
			};
			a.extend(c, f);
			b.data("block-data", c)
		}
		var f = "Jan,Feb,Mar,Apr,May,Jun,Jul,Aug,Sep,Oct,Nov,Dec".split(",");
		return {
			render: function() {
				for (var o = c.data, m = c.cellHeight, t = a("<div>", {
					"class": "ganttview-vtheader"
				}), q = 0; q < o.length; q++) {
					var w = a("<div>", {
						"class": "ganttview-vtheader-item"
					});
					w.append(a("<div>", {
						"class": "ganttview-vtheader-item-name",
						css: {
							height: o[q].series.length * m + "px"
						}
					}).append(o[q].name));
					var aa = a("<div>", {
						"class": "ganttview-vtheader-series"
					}),
					F = o[q].start,
					Ma = o[q].end;
					typeof F !== "undefined" && F !== false && typeof Ma !== "undefined" && Ma !== false && (aa.append(a("<div>", {
						"class": "ganttview-vtheader-series-name"
					}).append("")), w.append(aa));
					for (F = 0; F < o[q].series.length; F++) aa.append(a("<div>", {
						"class": "ganttview-vtheader-series-name"
					}).append(o[q].series[F].name));
					w.append(aa);
					t.append(w)
				}
				b.append(t);
				o = a("<div>", {
					"class": "ganttview-slide-container",
					css: {
						width: c.slideWidth + "px"
					}
				});
				q = c.start;
				m = c.end;
				t = [];
				t[q.getFullYear()] = [];
				for (t[q.getFullYear()][q.getMonth()] = [q]; q.compareTo(m) == - 1;) q = q.clone().addDays(1),
				t[q.getFullYear()] || (t[q.getFullYear()] = []),
				t[q.getFullYear()][q.getMonth()] || (t[q.getFullYear()][q.getMonth()] = []),
				t[q.getFullYear()][q.getMonth()].push(q);
				var m = dates = t,
				t = c.cellWidth,
				q = a("<div>", {
					"class": "ganttview-hzheader"
				}),
				w = a("<div>", {
					"class": "ganttview-hzheader-months"
				}),
				aa = a("<div>", {
					"class": "ganttview-hzheader-days"
				}),
				F = 0,
				M;
				for (M in m) for (var Q in m[M]) {
					Ma = m[M][Q].length * t;
					F += Ma;
					w.append(a("<div>", {
						"class": "ganttview-hzheader-month",
						css: {
							width: Ma - 1 + "px"
						}
					}).append(f[Q] + "/" + M));
					for (var A in m[M][Q]) aa.append(a("<div>", {
						"class": "ganttview-hzheader-day"
					}).append(m[M][Q][A].getDate()))
				}
				w.css("width", F + "px");
				aa.css("width", F + "px");
				q.append(w).append(aa);
				o.append(q);
				M = c.data;
				m = dates;
				t = c.cellWidth;
				q = c.showWeekends;
				Q = a("<div>", {
					"class": "ganttview-grid"
				});
				A = a("<div>", {
					"class": "ganttview-grid-row"
				});
				for (var v in m) for (var N in m[v]) for (var x in m[v][N]) w = a("<div>", {
					"class": "ganttview-grid-row-cell"
				}),
				h.isWeekend(m[v][N][x]) && q && w.addClass("ganttview-weekend"),
				A.append(w);
				v = a("div.ganttview-grid-row-cell", A).length * t;
				A.css("width", v + "px");
				Q.css("width", v + "px");
				for (v = 0; v < M.length; v++) {
					N = M[v].start;
					x = M[v].end;
					typeof N !== "undefined" && N !== false && typeof x !== "undefined" && x !== false && Q.append(A.clone());
					for (N = 0; N < M[v].series.length; N++) Q.append(A.clone())
				}
				o.append(Q);
				v = c.data;
				N = a("<div>", {
					"class": "ganttview-blocks"
				});
				for (x = 0; x < v.length; x++) {
					M = v[x].start;
					Q = v[x].end;
					typeof M !== "undefined" && M !== false && typeof Q !== "undefined" && Q !== false && N.append(a("<div>", {
						"class": "ganttview-block-container"
					}));
					for (M = 0; M < v[x].series.length; M++) N.append(a("<div>", {
						"class": "ganttview-block-container"
					}))
				}
				o.append(N);
				v = c.data;
				N = c.cellWidth;
				x = c.start;
				M = a("div.ganttview-blocks div.ganttview-block-container", o);
				for (A = Q = 0; A < v.length; A++) {
					t = v[A].start;
					m = v[A].end;
					typeof t !== "undefined" && t !== false && typeof m !== "undefined" && m !== false && (m = h.daysBetween(t, m) + 1, w = h.daysBetween(x, t), w = a("<div>", {
						"class": "ganttview-block",
						title: v[A].label + ", " + m + " days",
						css: {
							width: m * N - 9 + "px",
							"margin-left": w * N + 3 + "px"
						}
					}), d(w, v[A], [""]), v[A].color && w.css("background-color", v[A].color), w.append(a("<div>", {
						"class": "ganttview-block-text"
					}).text(m)), a(M[Q]).append(w), Q += 1);
					for (t = 0; t < v[A].series.length; t++) q = v[A].series[t],
					m = h.daysBetween(q.start, q.end) + 1,
					w = h.daysBetween(x, q.start),
					w = a("<div>", {
						"class": "ganttview-block",
						title: q.label + ", " + m + " days",
						css: {
							width: m * N - 9 + "px",
							"margin-left": w * N + 3 + "px"
						}
					}),
					d(w, v[A], q),
					v[A].series[t].color && w.css("background-color", v[A].series[t].color),
					w.append(a("<div>", {
						"class": "ganttview-block-text"
					}).text(m)),
					a(M[Q]).append(w),
					Q += 1
				}
				b.append(o);
				o = b.parent();
				a("div.ganttview-grid-row div.ganttview-grid-row-cell:last-child", o).addClass("last");
				a("div.ganttview-hzheader-days div.ganttview-hzheader-day:last-child", o).addClass("last");
				a("div.ganttview-hzheader-months div.ganttview-hzheader-month:last-child", o).addClass("last")
			}
		}
	},
	f = function(b, c) {
		function d(b, c) {
			a("div.ganttview-block", b).live("click", function() {
				c && c(a(this).data("block-data"))
			})
		}
		function f(b, c, d, g) {
			a("div.ganttview-block", b).resizable({
				grid: c,
				handles: "e,w",
				stop: function() {
					var f = a(this);
					m(b, f, c, d);
					g && g(f.data("block-data"))
				}
			})
		}
		function h(b, c, d, f) {
			a("div.ganttview-block", b).draggable({
				axis: "x",
				grid: [c, c],
				stop: function() {
					var g = a(this);
					m(b, g, c, d);
					f && f(g.data("block-data"))
				}
			})
		}
		function m(b, c, d, f) {
			var b = a("div.ganttview-slide-container", b),
			g = b.scrollLeft(),
			b = c.offset().left - b.offset().left - 1 + g,
			g = Math.round(b / d),
			f = f.clone().addDays(g);
			c.data("block-data").start = f;
			g = c.outerWidth();
			d = Math.round(g / d) - 1;
			c.data("block-data").end = f.clone().addDays(d);
			a("div.ganttview-block-text", c).text(d + 1);
			c.css("top", "").css("left", "").css("position", "relative").css("margin-left", b + "px")
		}
		return {
			apply: function() {
				c.behavior.clickable && d(b, c.behavior.onClick);
				c.behavior.resizable && f(b, c.cellWidth, c.start, c.behavior.onResize);
				c.behavior.draggable && h(b, c.cellWidth, c.start, c.behavior.onDrag)
			}
		}
	},
	h = {
		daysBetween: function(a, b) {
			if (!a || ! b) return 0;
			a = Date.parse(a);
			b = Date.parse(b);
			if (a.getYear() == 1901 || b.getYear() == 8099) return 0;
			for (var c = 0, d = a.clone(); d.compareTo(b) == - 1;) c += 1,
			d.addDays(1);
			return c
		},
		isWeekend: function(a) {
			return a.getDay() % 6 == 0
		},
		getBoundaryDatesFromData: function(a, b) {
			var c = new Date;
			maxEnd = new Date;
			for (var d = 0; d < a.length; d++) for (var f = 0; f < a[d].series.length; f++) {
				var m = Date.parse(a[d].series[f].start),
				t = Date.parse(a[d].series[f].end);
				d == 0 && f == 0 && (c = m, maxEnd = t);
				c.compareTo(m) == 1 && (c = m);
				maxEnd.compareTo(t) == - 1 && (maxEnd = t)
			}
			h.daysBetween(c, maxEnd) < b && (maxEnd = c.clone().addDays(b));
			return [c, maxEnd]
		}
	}
})(jQuery);
var qq = qq || {};
qq.extend = function(a, b) {
	for (var c in b) a[c] = b[c]
};
qq.indexOf = function(a, b, c) {
	if (a.indexOf) return a.indexOf(b, c);
	var c = c || 0,
	d = a.length;
	for (c < 0 && (c += d); c < d; c++) if (c in a && a[c] === b) return c;
	return - 1
};
qq.getUniqueId = function() {
	var a = 0;
	return function() {
		return a++
	}
} ();
qq.attach = function(a, b, c) {
	a.addEventListener ? a.addEventListener(b, c, false) : a.attachEvent && a.attachEvent("on" + b, c)
};
qq.detach = function(a, b, c) {
	a.removeEventListener ? a.removeEventListener(b, c, false) : a.attachEvent && a.detachEvent("on" + b, c)
};
qq.preventDefault = function(a) {
	a.preventDefault ? a.preventDefault() : a.returnValue = false
};
qq.insertBefore = function(a, b) {
	b.parentNode.insertBefore(a, b)
};
qq.remove = function(a) {
	a.parentNode.removeChild(a)
};
qq.contains = function(a, b) {
	return a == b ? true: a.contains ? a.contains(b) : !! (b.compareDocumentPosition(a) & 8)
};
qq.toElement = function() {
	var a = document.createElement("div");
	return function(b) {
		a.innerHTML = b;
		b = a.firstChild;
		a.removeChild(b);
		return b
	}
} ();
qq.css = function(a, b) {
	if (b.opacity != null && typeof a.style.opacity != "string" && typeof a.filters != "undefined") b.filter = "alpha(opacity=" + Math.round(100 * b.opacity) + ")";
	qq.extend(a.style, b)
};
qq.hasClass = function(a, b) {
	return RegExp("(^| )" + b + "( |$)").test(a.className)
};
qq.addClass = function(a, b) {
	qq.hasClass(a, b) || (a.className += " " + b)
};
qq.removeClass = function(a, b) {
	a.className = a.className.replace(RegExp("(^| )" + b + "( |$)"), " ").replace(/^\s+|\s+$/g, "")
};
qq.setText = function(a, b) {
	a.innerText = b;
	a.textContent = b
};
qq.children = function(a) {
	for (var b = [], a = a.firstChild; a;) a.nodeType == 1 && b.push(a),
	a = a.nextSibling;
	return b
};
qq.getByClass = function(a, b) {
	if (a.querySelectorAll) return a.querySelectorAll("." + b);
	for (var c = [], d = a.getElementsByTagName("*"), f = d.length, h = 0; h < f; h++) qq.hasClass(d[h], b) && c.push(d[h]);
	return c
};
qq.obj2url = function(a, b, c) {
	var d = [],
	f = "&",
	h = function(a, c) {
		var f = b ? /\[\]$/.test(b) ? b: b + "[" + c + "]": c;
		f != "undefined" && c != "undefined" && d.push(typeof a === "object" ? qq.obj2url(a, f, true) : Object.prototype.toString.call(a) === "[object Function]" ? encodeURIComponent(f) + "=" + encodeURIComponent(a()) : encodeURIComponent(f) + "=" + encodeURIComponent(a))
	};
	if (!c && b) f = /\?/.test(b) ? /\?$/.test(b) ? "": "&": "?",
	d.push(b),
	d.push(qq.obj2url(a));
	else if (Object.prototype.toString.call(a) === "[object Array]" && typeof a != "undefined") for (var n = 0, c = a.length; n < c; ++n) h(a[n], n);
	else if (typeof a != "undefined" && a !== null && typeof a === "object") for (n in a) h(a[n], n);
	else d.push(encodeURIComponent(b) + "=" + encodeURIComponent(a));
	return d.join(f).replace(/^&/, "").replace(/%20/g, "+")
};
qq = qq || {};
qq.FileUploaderBasic = function(a) {
	this._options = {
		debug: false,
		action: "/server/upload",
		params: {},
		button: null,
		multiple: true,
		maxConnections: 3,
		allowedExtensions: [],
		sizeLimit: 0,
		minSizeLimit: 0,
		onSubmit: function() {},
		onProgress: function() {},
		onComplete: function() {},
		onAllComplete: function() {},
		onCancel: function() {},
		messages: {
			typeError: "{file} has invalid extension. Only {extensions} are allowed.",
			sizeError: "{file} is too large, maximum file size is {sizeLimit}.",
			minSizeError: "{file} is too small, minimum file size is {minSizeLimit}.",
			emptyError: "{file} is empty, please select files again without it.",
			onLeave: "The files are being uploaded, if you leave now the upload will be cancelled."
		},
		showMessage: function(a) {
			alert(a)
		}
	};
	qq.extend(this._options, a);
	this._filesInProgress = 0;
	this._handler = this._createUploadHandler();
	if (this._options.button) this._button = this._createUploadButton(this._options.button);
	this._preventLeaveInProgress()
};
qq.FileUploaderBasic.prototype = {
	setParams: function(a) {
		this._options.params = a
	},
	getInProgress: function() {
		return this._filesInProgress
	},
	_createUploadButton: function(a) {
		var b = this;
		return new qq.UploadButton({
			element: a,
			multiple: this._options.multiple && qq.UploadHandlerXhr.isSupported(),
			onChange: function(a) {
				b._onInputChange(a)
			}
		})
	},
	_createUploadHandler: function() {
		var a = this,
		b;
		b = qq.UploadHandlerXhr.isSupported() ? "UploadHandlerXhr": "UploadHandlerForm";
		return new qq[b]({
			debug: this._options.debug,
			action: this._options.action,
			maxConnections: this._options.maxConnections,
			onProgress: function(b, d, f, h) {
				a._onProgress(b, d, f, h);
				a._options.onProgress(b, d, f, h)
			},
			onComplete: function(b, d, f) {
				a._onComplete(b, d, f);
				a._options.onComplete(b, d, f)
			},
			onAllComplete: function(b) {
				a._options.onAllComplete(b)
			},
			onCancel: function(b, d) {
				a._onCancel(b, d);
				a._options.onCancel(b, d)
			}
		})
	},
	_preventLeaveInProgress: function() {},
	_onSubmit: function() {
		this._filesInProgress++
	},
	_onProgress: function() {},
	_onComplete: function(a, b, c) {
		this._filesInProgress--;
		c.error && this._options.showMessage(c.error)
	},
	_onCancel: function() {
		this._filesInProgress--
	},
	_onInputChange: function(a) {
		this._handler instanceof qq.UploadHandlerXhr ? this._uploadFileList(a.files) : this._validateFile(a) && this._uploadFile(a);
		this._button.reset()
	},
	_uploadFileList: function(a) {
		for (var b = 0; b < a.length; b++) if (!this._validateFile(a[b])) return;
		for (b = 0; b < a.length; b++) this._uploadFile(a[b])
	},
	_uploadFile: function(a) {
		var a = this._handler.add(a),
		b = this._handler.getName(a);
		this._options.onSubmit(a, b) !== false && (this._onSubmit(a, b), this._handler.upload(a, this._options.params))
	},
	_validateFile: function(a) {
		var b, c;
		a.value ? b = a.value.replace(/.*(\/|\\)/, "") : (b = a.fileName != null ? a.fileName: a.name, c = a.fileSize != null ? a.fileSize: a.size);
		if (this._isAllowedExtension(b)) if (c === 0) return this._error("emptyError", b),
		false;
		else if (c && this._options.sizeLimit && c > this._options.sizeLimit) return this._error("sizeError", b),
		false;
		else {
			if (c && c < this._options.minSizeLimit) return this._error("minSizeError", b),
			false
		} else return this._error("typeError", b),
		false;
		return true
	},
	_error: function(a, b) {
		var c = this._options.messages[a],
		d = this._formatFileName(b),
		c = c.replace("{file}", d),
		d = this._options.allowedExtensions.join(", "),
		c = c.replace("{extensions}", d),
		d = this._formatSize(this._options.sizeLimit),
		c = c.replace("{sizeLimit}", d),
		d = this._formatSize(this._options.minSizeLimit),
		c = c.replace("{minSizeLimit}", d);
		this._options.showMessage(c)
	},
	_formatFileName: function(a) {
		a.length > 33 && (a = a.slice(0, 19) + "..." + a.slice( - 13));
		return a
	},
	_isAllowedExtension: function(a) {
		var a = - 1 !== a.indexOf(".") ? a.replace(/.*[.]/, "").toLowerCase() : "",
		b = this._options.allowedExtensions;
		if (!b.length) return true;
		for (var c = 0; c < b.length; c++) if (b[c].toLowerCase() == a) return true;
		return false
	},
	_formatSize: function(a) {
		var b = - 1;
		do a /= 1024,
		b++;
		while (a > 99);
		return Math.max(a, 0.1).toFixed(1) + "kB,MB,GB,TB,PB,EB".split(",")[b]
	}
};
qq.FileUploader = function(a) {
	qq.FileUploaderBasic.apply(this, arguments);
	qq.extend(this._options, {
		element: null,
		listElement: null,
		template: '<span class="qq-uploader"><span class="qq-upload-button">' + a.text.attach + '</span><ul class="qq-upload-list"></ul></span>',
		fileTemplate: '<li><span class="qq-upload-file"></span><span class="qq-upload-spinner"></span><span class="qq-upload-size"></span><a class="qq-upload-cancel" href="#">' + a.text.cancel + '</a><span class="qq-upload-failed-text">' + a.text.failed + "</span></li>",
		classes: {
			button: "qq-upload-button",
			list: "qq-upload-list",
			file: "qq-upload-file",
			spinner: "qq-upload-spinner",
			size: "qq-upload-size",
			cancel: "qq-upload-cancel",
			success: "qq-upload-success",
			fail: "qq-upload-fail"
		}
	});
	qq.extend(this._options, a);
	this._element = this._options.element;
	this._element.innerHTML = this._options.template;
	this._listElement = this._options.listElement || this._find(this._element, "list");
	this._classes = this._options.classes;
	this._button = this._createUploadButton(this._find(this._element, "button"));
	this._bindCancelEvent();
	this._setupDragDrop()
};
qq.extend(qq.FileUploader.prototype, qq.FileUploaderBasic.prototype);
qq.extend(qq.FileUploader.prototype, {
	_find: function(a, b) {
		var c = qq.getByClass(a, this._options.classes[b])[0];
		if (!c) throw Error("element not found " + b);
		return c
	},
	_setupDragDrop: function() {},
	_onSubmit: function(a, b) {
		qq.FileUploaderBasic.prototype._onSubmit.apply(this, arguments);
		this._addToList(a, b)
	},
	_onProgress: function(a, b, c, d) {
		qq.FileUploaderBasic.prototype._onProgress.apply(this, arguments);
		var f = this._find(this._getItemByFileId(a), "size");
		f.style.display = "inline";
		var h;
		h = c != d ? Math.round(c / d * 100) + "% from " + this._formatSize(d) : this._formatSize(d);
		qq.setText(f, h)
	},
	_onComplete: function(a, b, c) {
		qq.FileUploaderBasic.prototype._onComplete.apply(this, arguments);
		var d = this._getItemByFileId(a);
		qq.remove(this._find(d, "cancel"));
		qq.remove(this._find(d, "spinner"));
		c.success ? $(d).slideUp(300) : qq.innerHTML = ""
	},
	_addToList: function(a, b) {
		var c = qq.toElement(this._options.fileTemplate);
		c.qqFileId = a;
		var d = this._find(c, "file");
		qq.setText(d, this._formatFileName(b));
		qq.setText(d, this._formatFileName(b));
		this._find(c, "size").style.display = "none";
		this._listElement.appendChild(c)
	},
	_getItemByFileId: function(a) {
		for (var b = this._listElement.firstChild; b;) {
			if (b.qqFileId == a) return b;
			b = b.nextSibling
		}
	},
	_bindCancelEvent: function() {
		var a = this;
		qq.attach(this._listElement, "click", function(b) {
			var b = b || window.event,
			c = b.target || b.srcElement;
			if (qq.hasClass(c, a._classes.cancel)) qq.preventDefault(b),
			b = c.parentNode,
			a._handler.cancel(b.qqFileId),
			qq.remove(b)
		})
	}
});
qq.UploadDropZone = function() {};
qq.UploadButton = function(a) {
	this._options = {
		element: null,
		multiple: false,
		name: "file",
		onChange: function() {},
		hoverClass: "qq-upload-button-hover",
		focusClass: "qq-upload-button-focus"
	};
	qq.extend(this._options, a);
	this._element = this._options.element;
	qq.css(this._element, {
		position: "relative",
		overflow: "hidden",
		direction: "ltr"
	});
	this._input = this._createInput()
};
qq.UploadButton.prototype = {
	getInput: function() {
		return this._input
	},
	reset: function() {
		this._input.parentNode && qq.remove(this._input);
		qq.removeClass(this._element, this._options.focusClass);
		this._input = this._createInput()
	},
	_createInput: function() {
		var a = document.createElement("input");
		this._options.multiple && a.setAttribute("multiple", "multiple");
		a.setAttribute("type", "file");
		a.setAttribute("name", this._options.name);
		qq.css(a, {
			position: "absolute",
			right: 0,
			top: "6px",
			fontFamily: "Arial",
			fontSize: "2px",
			margin: 0,
			padding: 0,
			cursor: "pointer",
			opacity: 0
		});
		this._element.appendChild(a);
		var b = this;
		qq.attach(a, "change", function() {
			b._options.onChange(a)
		});
		qq.attach(a, "mouseover", function() {
			qq.addClass(b._element, b._options.hoverClass)
		});
		qq.attach(a, "mouseout", function() {
			qq.removeClass(b._element, b._options.hoverClass)
		});
		qq.attach(a, "focus", function() {
			qq.addClass(b._element, b._options.focusClass)
		});
		qq.attach(a, "blur", function() {
			qq.removeClass(b._element, b._options.focusClass)
		});
		window.attachEvent && a.setAttribute("tabIndex", "-1");
		return a
	}
};
qq.UploadHandlerAbstract = function(a) {
	this._options = {
		debug: false,
		action: "/upload.php",
		maxConnections: 999,
		onProgress: function() {},
		onComplete: function() {},
		onAllComplete: function() {},
		onCancel: function() {}
	};
	qq.extend(this._options, a);
	this._queue = [];
	this._params = [];
	this._completed_files = []
};
qq.UploadHandlerAbstract.prototype = {
	log: function(a) {
		this._options.debug && window.console && console.log("[uploader] " + a)
	},
	add: function() {},
	upload: function(a, b) {
		var c = this._queue.push(a),
		d = {};
		qq.extend(d, b);
		this._params[a] = d;
		c <= this._options.maxConnections && this._upload(a, this._params[a])
	},
	cancel: function(a) {
		this._cancel(a);
		this._dequeue(a)
	},
	cancelAll: function() {
		for (var a = 0; a < this._queue.length; a++) this._cancel(this._queue[a]);
		this._queue = []
	},
	getName: function() {},
	getSize: function() {},
	getQueue: function() {
		return this._queue
	},
	_upload: function() {},
	_cancel: function() {},
	_dequeue: function(a) {
		this._queue.splice(qq.indexOf(this._queue, a), 1);
		a = this._options.maxConnections;
		this._queue.length >= a && (a = this._queue[a - 1], this._upload(a, this._params[a]));
		this._queue.length == 0 && this._onAllComplete()
	},
	_onAllComplete: function() {
		this._options.onAllComplete(this._completed_files)
	}
};
qq.UploadHandlerForm = function(a) {
	qq.UploadHandlerAbstract.apply(this, arguments);
	this._inputs = {}
};
qq.extend(qq.UploadHandlerForm.prototype, qq.UploadHandlerAbstract.prototype);
qq.extend(qq.UploadHandlerForm.prototype, {
	add: function(a) {
		a.setAttribute("name", "qqfile");
		var b = "qq-upload-handler-iframe" + qq.getUniqueId();
		this._inputs[b] = a;
		a.parentNode && qq.remove(a);
		return b
	},
	getName: function(a) {
		return this._inputs[a].value.replace(/.*(\/|\\)/, "")
	},
	_cancel: function(a) {
		this._options.onCancel(a, this.getName(a));
		delete this._inputs[a];
		if (a = document.getElementById(a)) a.setAttribute("src", "javascript:false;"),
		qq.remove(a)
	},
	_upload: function(a, b) {
		var c = this._inputs[a];
		if (!c) throw Error("file with passed id was not added, or already uploaded or cancelled");
		var d = this.getName(a),
		f = this._createIframe(a),
		h = this._createForm(f, b);
		h.appendChild(c);
		var n = this;
		this._attachLoadEvent(f, function() {
			n.log("iframe loaded");
			var b = n._getIframeContentJSON(f);
			n._options.onComplete(a, d, b);
			n._dequeue(a);
			delete n._inputs[a];
			setTimeout(function() {
				qq.remove(f)
			},
			1)
		});
		h.submit();
		qq.remove(h);
		return a
	},
	_attachLoadEvent: function(a, b) {
		qq.attach(a, "load", function() {
			a.parentNode && (!a.contentDocument || ! (a.contentDocument.body && a.contentDocument.body.innerHTML == "false")) && b()
		})
	},
	_getIframeContentJSON: function(a) {
		var a = a.contentDocument ? a.contentDocument: a.contentWindow.document,
		b;
		this.log("converting iframe's innerHTML to JSON");
		this.log("innerHTML = " + a.body.innerHTML);
		var c = document.createElement("div");
		c.innerHTML = a.body.innerHTML;
		a = c.textContent;
		try {
			b = eval("(" + a + ")")
		} catch(d) {
			b = $.parseJSON(a)
		}
		return b
	},
	_createIframe: function(a) {
		var b = qq.toElement('<iframe src="javascript:false;" name="' + a + '" />');
		b.setAttribute("id", a);
		b.style.display = "none";
		document.body.appendChild(b);
		return b
	},
	_createForm: function(a, b) {
		var c = null,
		c = b.csrf_token && b.csrf_name ? qq.toElement('<form method="post" enctype="multipart/form-data">' + ('<input type="hidden" name="' + b.csrf_name + '" value="' + b.csrf_token + '" />') + "</form>") : qq.toElement('<form method="post" enctype="multipart/form-data"></form>');
		delete b.csrf_token;
		delete b.csrf_name;
		delete b.csrf_xname;
		var d = qq.obj2url(b, this._options.action);
		c.setAttribute("action", d);
		c.setAttribute("target", a.name);
		c.style.display = "none";
		document.body.appendChild(c);
		return c
	}
});
qq.UploadHandlerXhr = function(a) {
	qq.UploadHandlerAbstract.apply(this, arguments);
	this._files = [];
	this._xhrs = [];
	this._loaded = []
};
qq.UploadHandlerXhr.isSupported = function() {
	var a = document.createElement("input");
	a.type = "file";
	return "multiple" in a && typeof File != "undefined" && typeof(new XMLHttpRequest).upload != "undefined"
};
qq.extend(qq.UploadHandlerXhr.prototype, qq.UploadHandlerAbstract.prototype);
qq.extend(qq.UploadHandlerXhr.prototype, {
	add: function(a) {
		if (! (a instanceof File)) throw Error("Passed obj is not a File (in qq.UploadHandlerXhr)");
		return this._files.push(a) - 1
	},
	getName: function(a) {
		a = this._files[a];
		return a.fileName != null ? a.fileName: a.name
	},
	getSize: function(a) {
		a = this._files[a];
		return a.fileSize != null ? a.fileSize: a.size
	},
	getLoaded: function(a) {
		return this._loaded[a] || 0
	},
	_upload: function(a, b) {
		var c = this._files[a],
		d = this.getName(a);
		this.getSize(a);
		this._loaded[a] = 0;
		var f = this._xhrs[a] = new XMLHttpRequest,
		h = this;
		f.upload.onprogress = function(b) {
			if (b.lengthComputable) h._loaded[a] = b.loaded,
			h._options.onProgress(a, d, b.loaded, b.total)
		};
		f.onreadystatechange = function() {
			f.readyState == 4 && h._onComplete(a, f)
		};
		var b = b || {},
		n = false,
		g = false;
		if (b.csrf_token && b.csrf_xname) n = b.csrf_token,
		g = b.csrf_xname,
		delete b.csrf_token,
		delete b.csrf_xname,
		delete b.csrf_name;
		b.qqfile = d;
		var p = qq.obj2url(b, this._options.action);
		f.open("POST", p, true);
		f.setRequestHeader("X-Requested-With", "XMLHttpRequest");
		f.setRequestHeader("X-File-Name", encodeURIComponent(d));
		f.setRequestHeader("Content-Type", "application/octet-stream");
		n && f.setRequestHeader(g, n);
		f.send(c)
	},
	_onComplete: function(a, b) {
		if (this._files[a]) {
			var c = this.getName(a),
			d = this.getSize(a);
			this._options.onProgress(a, c, d, d);
			if (b.status == 200 || b.status == 201) {
				this.log("xhr - server response received");
				this.log("responseText = " + b.responseText);
				var f;
				try {
					f = eval("(" + b.responseText + ")")
				} catch(h) {
					f = {}
				}
				this._completed_files.push({
					file: this._files[a],
					response: f
				});
				this._options.onComplete(a, c, f)
			} else this._completed_files.push({
				file: this._files[a],
				response: {}
			}),
			this._options.onComplete(a, c, {});
			this._files[a] = null;
			this._xhrs[a] = null;
			this._dequeue(a)
		}
	},
	_cancel: function(a) {
		this._options.onCancel(a, this.getName(a));
		this._files[a] = null;
		this._xhrs[a] && (this._xhrs[a].abort(), this._xhrs[a] = null)
	}
});
(function(a) {
	a.fn.tipsy = function(b) {
		b = a.extend({},
		a.fn.tipsy.defaults, b);
		return this.each(function() {
			var c = a.fn.tipsy.elementOptions(this, b);
			a(this).hover(function() {
				a.data(this, "cancel.tipsy", true);
				var b = a.data(this, "active.tipsy");
				b || (b = a('<div class="tipsy"><div class="tipsy-inner"/></div>'), b.css({
					position: "absolute",
					zIndex: 1E5
				}), a.data(this, "active.tipsy", b));
				if (a(this).attr("title") || typeof a(this).attr("original-title") != "string") a(this).attr("original-title", a(this).attr("title") || "").removeAttr("title");
				var f;
				typeof c.title == "string" ? f = a(this).attr(c.title == "title" ? "original-title": c.title) : typeof c.title == "function" && (f = c.title.call(this));
				b.find(".tipsy-inner")[c.html ? "html": "text"](f || c.fallback);
				f = a.extend({},
				a(this).offset(), {
					width: this.offsetWidth,
					height: this.offsetHeight
				});
				b.get(0).className = "tipsy";
				b.remove().css({
					top: 0,
					left: 0,
					visibility: "hidden",
					display: "block"
				}).appendTo(document.body);
				var h = b[0].offsetWidth,
				n = b[0].offsetHeight;
				switch ((typeof c.gravity == "function" ? c.gravity.call(this) : c.gravity).charAt(0)) {
				case "n":
					b.css({
						top:
						f.top + f.height,
						left: f.left + f.width / 2 - h / 2
					}).addClass("tipsy-north");
					break;
				case "s":
					b.css({
						top:
						f.top - n,
						left: f.left + f.width / 2 - h / 2
					}).addClass("tipsy-south");
					break;
				case "e":
					b.css({
						top:
						f.top + f.height / 2 - n / 2,
						left: f.left - h
					}).addClass("tipsy-east");
					break;
				case "w":
					b.css({
						top:
						f.top + f.height / 2 - n / 2,
						left: f.left + f.width
					}).addClass("tipsy-west")
				}
				c.fade ? b.css({
					opacity: 0,
					display: "block",
					visibility: "visible"
				}).animate({
					opacity: 0.8
				}) : b.css({
					visibility: "visible"
				})
			},
			function() {
				a.data(this, "cancel.tipsy", false);
				var b = this;
				setTimeout(function() {
					if (!a.data(this, "cancel.tipsy")) {
						var f = a.data(b, "active.tipsy");
						c.fade ? f.stop().fadeOut(function() {
							a(this).remove()
						}) : f.remove()
					}
				},
				100)
			})
		})
	};
	a.fn.tipsy.elementOptions = function(b, c) {
		return a.metadata ? a.extend({},
		c, a(b).metadata()) : c
	};
	a.fn.tipsy.defaults = {
		fade: false,
		fallback: "",
		gravity: "n",
		html: false,
		title: "title"
	};
	a.fn.tipsy.autoNS = function() {
		return a(this).offset().top > a(document).scrollTop() + a(window).height() / 2 ? "s": "n"
	};
	a.fn.tipsy.autoWE = function() {
		return a(this).offset().left > a(document).scrollLeft() + a(window).width() / 2 ? "e": "w"
	}
})(jQuery);

