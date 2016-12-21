function t(t) {
    var a = t;
    return void 0 == stats_translation[t] ? console.log(t) : a = stats_translation[t][current_language], a
}

function setItemPotentialsBuild(t, a) {
    loader.init();
    var e = [];
    $("#equip-stats .equip").each(function() {
        var a = $(this),
            i = $(a).find(".item-rarity select").val();
        if ("" != i) {
            var s = $(a).data("type"),
                n = $(a).find(".potentials"),
                o = JSON.parse(JSON.stringify(t));
            $(n).find(".potential").each(function() {
                var t = $(this).find(".potential-stat select"),
                    a = !1;
                for (var i in o[s]) {
                    var n = o[s][i];
                    if (a) return;
                    $(t).find("option[value='" + n + "']").length && ($(t).val(n), e.push(getEquipPotentials(t)), delete o[s][i], a = !0)
                }
            })
        }
    }), $.when.apply(null, e).done(function() {
        $(".potential-val select option[data-level='" + a + "']").attr("selected", "selected"), applyAllBgRarity(), calculatePls(), loader.stop()
    })
}

function setSet(t, a) {
    $(t).find(".set select").each(function() {
        $(this).val(a), getSetStuff($(this))
    });
    var e = $(t).find(".platinum input");
    setPlatinum("", e)
}

function filterSets() {
    var t = $("#sets-filter input").val(),
        a = $("#sets-list .set-info");
    if ($(a).show(), "" != t || 0 != $("#sets-filter button.active").length) {
        var e = "";
        $("#sets-filter button.active").each(function() {
            var t = $(this).data("type"),
                a = $(this).data("stuff");
            e += "[data-" + t + "='" + a + "']"
        }), "" != e && $("#sets-list .set-info:not(" + e + ")").hide(), "" != t && $("#sets-list .set-info:visible").each(function() {
            0 == $(this).find("span.effect:contains('" + t + "')").length && 0 == $(this).find("span.title:contains('" + t + "')").length && $(this).hide()
        })
    }
}

function displayIllustration() {
    var t = $("#select-hero").val();
    "" != t ? $("body").css("background-image", "url(assets/images/illust/" + t + ".png)") : $("body").css("background-image", "url(assets/images/bg/yekaterina-by-fizintine.jpg)")
}

function resetEquips() {
    $("#equip-stats .equip").each(function() {
        $(this).find(".set select, .stuff select, .item-rarity select, .enhancement select").val("").attr("class", "form-control").removeAttr("disabled"), $(this).find(".item-rarity select").addClass("rarity").change(), setPlatinum(0)
    })
}

function resetPotentials() {
    $("#equip-stats .potential-stat select").each(function() {
        $(this).val("").attr("class", "form-control"), updateEquipPotential(this), getEquipPotentials(this)
    }), $(".btn-action-container").remove()
}

function addCloneButton(t) {
    var a = $(t).closest(".potential"),
        e = $(a).find(".potential-stat select").val();
    if ("" == e) return void $(a).find(".btn-action-container").remove();
    if (!$(a).find(".btn-action-container").length) {
        var i = $("<div>").addClass("btn-action-container"),
            s = $("<div>").addClass("btn-action action-clone-potential").html("<span class='glyphicon glyphicon-fullscreen'></span>");
        $(i).append(s), $(a).append(i)
    }
}

function cloneEquipPotential(t) {
    var a = $(t).closest(".potential"),
        e = $(a).find(".potential-stat select").val(),
        i = $(a).find(".potential-val select option:selected").data("level");
    if ("" != e) {
        var s = [];
        loader.init(), $("#equip-stats .equip").each(function() {
            var t = $(this);
            if (0 != $(t).find(".potential-stat select:not(:disabled) option[value='" + e + "']").length && !$(t).find(".potential-stat select option[value='" + e + "']:selected").length) {
                var a = !1;
                $(t).find(".potential-stat select").each(function() {
                    "" != $(this).val() || a || (a = !0, $(this).val(e), addCloneButton(this), s.push(getEquipPotentials(this)))
                })
            }
        }), i = "" == i ? 0 : i, $.when.apply(null, s).done(function() {
            $("#equip-stats .potential-stat select option[value='" + e + "']:selected").closest(".potential").find(".potential-val select option[data-level='" + i + "']").attr("selected", "selected"), applyAllBgRarity(), calculatePls(), loader.stop()
        })
    }
}

function setPlatinum(t, a) {
    a = void 0 == a || "" == a ? "#equip-stats .platinum input" : a;
    var e = [];
    loader.init(), t = 1 != t ? "" : 1, $(a).val(t).each(function() {
        updateItemSelects(this), displayPlatinum(this), e.push(getEquipStats(this))
    }), $.when.apply(null, e).done(function() {
        calculatePls(), loader.stop()
    })
}

function setEquipRarity(t) {
    $("#equip-stats .item-rarity select").each(function() {
        var a = $(this).closest(".equip"),
            e = $(a).find(".set select").val(),
            i = $(a).find(".platinum input").val();
        ("transcended" != t || "" != e || 0 != i) && ($(this).val(t), updateItemSelects(this))
    }), applyAllBgRarity()
}

function setEnhancement(t) {
    var a = [];
    loader.init(), $("#equip-stats .enhancement select").each(function() {
        var e = $(this).closest(".equip"),
            i = $(e).find(".platinum input").val(),
            s = $(e).find(".rarity option:selected"),
            n = $(s).data("minenhancement") || 0,
            o = $(s).data("maxenhancement") || 0;
        n > t || t > o || i && 13 == t || ($(this).val(t), a.push(getEquipStats(this)))
    }), $.when.apply(null, a).done(function() {
        calculatePls(), loader.stop()
    })
}

function setEquipStuff(t, a) {
    var e = [];
    loader.init(), $("#equip-stats .equip[data-type='" + t + "'] .set select").val(""), $("#equip-stats .equip[data-type='" + t + "'] .stuff select").val(a).removeAttr("disabled").each(function() {
        updateItemSelects(this), e.push(getEquipStats(this))
    }), $.when.apply(null, e).done(function() {
        calculatePls(), loader.stop()
    })
}

function toggleStatsTable(t) {
    $(t).hasClass("active") || ($(t).parent().find("button").removeClass("active"), $(t).addClass("active"), checkStatsTableDisplay())
}

function togglePlatinum(t) {
    target = $(t).data("target"), platinum = $("#" + target), platinumVal = $(platinum).val(), $(platinum).val(1 == platinumVal ? "" : 1), displayPlatinum(platinum)
}

function displayPlatinum(t) {
    platinum = $(t).closest(".platinum"), img = $(platinum).find("img"), equip = $(platinum).closest(".equip"), set = $(equip).find(".set select"), stuff = $(equip).find(".stuff select"), 1 == $(t).val() ? ($(img).addClass("active"), $(set).attr("disabled", !0).val(""), $(stuff).removeAttr("disabled")) : ($(img).removeClass("active"), $(set).removeAttr("disabled"))
}

function openImportDialog() {
    emptyModal();
    var t = $("#modal-calc");
    $(t).find(".modal-title").text("Import JSON data");
    var a = $("<textarea class='form-control' id='calc-json-textarea' rows='10'></textarea>");
    $(t).find(".modal-body").append(a), $button = $("<button id='btn-calc-import' class='btn btn-primary'>Import</button>"), $(t).find(".modal-footer").append($button), $(t).modal("show")
}

function openExportDialog() {
    emptyModal(), json = toJSONpls();
    var t = $("#modal-calc");
    $(t).find(".modal-title").text("Export JSON data");
    var a = $("<textarea class='form-control' id='calc-json-textarea' rows='10'></textarea>").val(json);
    $(t).find(".modal-body").append(a), $(t).modal("show")
}

function emptyModal() {
    var t = $("#modal-calc");
    $(t).find(".modal-title").empty(), $(t).find(".modal-body").empty(), $(t).find(".modal-footer button:not(.btn-close)").remove()
}

function displayCostumes() {
    var t = $("#select-hero").val();
    $("#hero-costumes > div").hide(), "" != t && $("#hero-costumes ." + t).show()
}

function displaySoulGears() {
    var t = $("#select-hero").val();
    $("#hero-soul-gears > div").hide(), "" != t && $("#hero-soul-gears ." + t).show()
}

function displayHeroPotential(t) {
    if (void 0 === t) $("#hero-potentials .potential").each(function() {
        var t = $(this),
            a = ($(t).data("num"), $(t).find(".potential-stat select").val());
        "-1" != a && ($(t).find(".potential-val select").hide(), $(t).find(".potential-val select[data-stat='" + a + "']").length && $(t).find(".potential-val select[data-stat='" + a + "']").show()), $(t).find(".potential-val select:hidden").val("")
    });
    else {
        var a = $("#hero-potentials .potential[data-num='" + t + "']"),
            e = $(a).find(".potential-stat select").val();
        "-1" != e && ($(a).find(".potential-val select").hide(), $(a).find(".potential-val select[data-stat='" + e + "']").length && $(a).find(".potential-val select[data-stat='" + e + "']").show()), $(a).find(".potential-val select:hidden").val("")
    }
}

function updateItemSelects(t) {
    var a = $(t).closest(".equip"),
        e = $(a).find(".item-rarity select"),
        s = $(e).find("option:selected").data("minenhancement") || 0,
        n = $(e).find("option:selected").data("maxenhancement") || 0,
        o = $(e).find("option:selected").data("maxpotential") || 0,
        l = $(a).find(".platinum input").val(),
        d = $(a).find(".set select").val();
    for (n = l && "transcended" == $(e).val() ? 12 : n, "" == d && 0 == l ? (s = 0, n = 10, $(e).find("option[value='transcended']").hide(), "transcended" == $(e).val() && ($(e).val(""), applyBgRarity(e))) : $(e).find("option[value='transcended']").show(), $(a).find(".enhancement select").val() > n && ($(a).find(".enhancement select").val(n), getEquipStats(t)), $(a).find(".enhancement select").val() < s && ($(a).find(".enhancement select").val(s), getEquipStats(t)), i = 0; 13 >= i; i++) $(a).find(".enhancement option[value='" + i + "']").show();
    for (i = 0; s > i; i++) $(a).find(".enhancement option[value='" + i + "']").hide();
    for (i = n + 1; 13 >= i; i++) $(a).find(".enhancement option[value='" + i + "']").hide();
    for (i = 0; o >= i; i++) $(a).find(".potential[data-num='" + i + "']").find("select").removeAttr("disabled");
    for (i = o + 1; 10 >= i; i++) {
        var r = $(a).find(".potential[data-num='" + i + "']");
        $(r).find("select").attr("disabled", !0).val(""), $(r).find(".btn-action-container").remove()
    }
}

function updateEquipPotential(t) {
    var a = $(t).closest(".potentials"),
        e = {};
    $(a).find(".potential").each(function() {
        var t = $(this).find(".potential-stat select").val();
        $(this).find("option").show(), "" != t && (e[t] = !0)
    });
    for (var i in e) $(a).find("option[value='" + i + "']").hide()
}

function getSetStuff(t) {
    var a = $(t).closest(".equip"),
        e = $(a).data("grade"),
        i = $(a).data("type"),
        s = $(t).val(),
        n = $("#sets-list .set-info[data-id='" + s + "']").data(i),
        o = $(a).find(".stuff select");
    $(o).removeAttr("disabled"), "" == !$(t).val() && $(o).val(n).attr("disabled", "true"), updateActiveSets(e)
}

function updateActiveSets(t) {
    t = void 0 == t || "" == t ? null : t, null != t ? ($("#sets-list .set-info[data-grade='" + t + "']").removeClass("active"), $(".equip[data-grade='" + t + "'] .set select").each(function() {
        var t = $(this).val();
        "" != t && $("#sets-list .set-info[data-id='" + t + "']").addClass("active")
    })) : ($("#sets-list .set-info").removeClass("active"), $(".equip .set select").each(function() {
        var t = $(this).val();
        "" != t && $("#sets-list .set-info[data-id='" + t + "']").addClass("active")
    }))
}

function getEquipStats(t) {
    var a = $(t).closest(".equip"),
        e = $(a).find(".stuff select").val(),
        s = $(a).find(".enhancement select").val(),
        n = $(a).find(".item-rarity select").val(),
        o = $(a).find(".platinum input").val(),
        l = $(a).find(".set select").val(),
        d = $("#sets-list .set-info[data-id='" + l + "']").data("rank"),
        r = $(a).find(".stats");
    if ("" == e || "" == s || "" == n) return void $(r).html("<i>Use dropdowns above</i>");
    var c = $.ajax({
        method: "POST",
        url: "data.equip-stats.php",
        data: {
            action: "getStats",
            grade: $(a).data("grade"),
            type: $(a).data("type"),
            stuff: e,
            enhancement: s,
            rarity: n,
            rank: d,
            platinum: o
        }
    }).done(function(t) {
        var a = JSON.parse(t);
        if (a.success) {
            var e = "";
            if (0 == a.stat.length) return;
            for (i = 0; i < a.stat.length; i++)
                for (var s in a.stat[i]) e += "<div class='stat' data-stat='" + tdf(s) + "' data-val='" + a.stat[i][s] + "'>" + s + " : " + a.stat[i][s] + "</div>";
            $(r).html(e)
        } else $(r).html("<i>No stat for this combo</i>")
    });
    return c
}

function getEquipPotentials(t) {
    var a = $(t).val(),
        e = $(t).closest(".equip"),
        s = $(t).closest(".potential"),
        n = $(e).data("grade"),
        o = $(e).data("type"),
        l = $(s).data("num"),
        d = $(s).find(".potential-val");
    if ("" == n || "" == a) return void $(d).html("<i>&lt;&lt; Use dropdowns</i>");
    var r = $.ajax({
        method: "POST",
        url: "data.equip-stats.php",
        data: {
            action: "getEquipPotentials",
            grade: n,
            stat: a
        }
    }).done(function(t) {
        var a = JSON.parse(t);
        if (a.success) {
            if (0 == a.list.length) return;
            var e = "<select class='form-control rarity' name='equip[" + n + "][" + o + "][potentials][" + l + "][val]'>";
            for (e += "<option class='bg-normal'></option>", i = 0; i < a.list.length; i++) e += "<option class='bg-" + a.list[i].rarity + "' value='" + a.list[i].value + "' data-level='" + a.list[i].level + "'>" + a.list[i].value + "</option>";
            e += "</select>", $(d).html(e)
        } else $(d).html("<i>??</i>")
    });
    return r
}

function populateItemPotentials(t) {
    data = JSON.parse(t);
    for (var a in data) - 1 != a.indexOf("][potentials]") && $("select[name='" + a + "']").val(data[a])
}

function applyAllBgRarity() {
    $("select.rarity:visible").each(function() {
        applyBgRarity(this)
    })
}

function applyBgRarity(t) {
    var a = $(t).val(),
        e = $(t).find("option[value='" + a + "']").attr("class");
    void 0 != e && "" != e && $(t).attr("class", "form-control rarity " + e), $(t).parent().hasClass("potential-val") && $(t).closest(".potential").find(".potential-stat select").attr("class", "form-control rarity " + e)
}

function loadCalcFromJSON(t) {
    loader.init(), populateFields(t), displayIllustration(), displayCostumes(), displaySoulGears(), displayHeroPotential(), $(".equip .set select").each(function() {
        getSetStuff(this)
    }), $(".equip .item-rarity select").each(function() {
        updateItemSelects(this), getEquipStats(this)
    }), $(".equip .platinum input").each(function() {
        displayPlatinum(this)
    });
    var a = [];
    $(".equip .potential-stat select").each(function() {
        var t = this;
        updateEquipPotential(t), "" != $(t).val() && a.push(getEquipPotentials(t))
    }), $.when.apply(null, a).done(function() {
        populateItemPotentials(t), applyAllBgRarity(), calculatePls(), loader.stop()
    })
}

function buildNotification(t, a, e, i) {
    var s = 5e3;
    $(".notif").length && $(".notif").remove(), void 0 === i && (i = !1);
    var n = $("<div></div>");
    $(n).addClass("notif alert alert-dismissible fade in alert-" + t), $(n).append("<button type='button' class='close' data-dismiss='alert' aria-label='Close'><span aria-hidden='true'>&times;</span></button>"), void 0 !== e && $(n).append("<h4>" + e + "</h4>"), $(n).append("<p>" + a + "</p>"), $("body > div.container:first, body > div.container-fluid:first").prepend(n), i && setTimeout(function() {
        $(".alert").fadeOut(1e3)
    }, s)
}

function calculatePls() {
    var t = {},
        a = {},
        e = {},
        i = {},
        s = [],
        n = [],
        o = $("#select-hero").val(),
        l = $("#select-hero option:selected"),
        d = "",
        r = 0,
        c = 30;
    if ("" != o) {
        $("#hero-stats #hero-stats-details #stats-table tr.stat:not(.stat-add)").each(function() {
            var a = $(this).data("stat"),
                e = $("#hero-" + tdf(a)).val();
            t[a] = parseFloat(e) || 0
        }), $("#hero-soul-gears ." + o + " .costume.active .stats").each(function() {
            var a = $(this).data();
            for (d in a) t[d] = t[d] + parseFloat(a[d]) || parseFloat(a[d])
        }), $("#hero-costumes ." + o + " .costume.active .stats").each(function() {
            var a = $(this).data();
            for (d in a) t[d] = t[d] + parseFloat(a[d]) || parseFloat(a[d])
        }), $("#hero-potentials .potential").each(function() {
            var a = $(this),
                e = $(a).find(".potential-stat select").val();
            null != e && -1 != e && void 0 != e && (O = $(a).find(".potential-val select:visible").val(), t[e] = t[e] + parseFloat(O) || t[e] + 0)
        }), $("#lord-costumes .costume.active .stats").each(function() {
            var a = $(this).data();
            for (d in a) t[d] = t[d] + parseFloat(a[d]) || parseFloat(a[d])
        }), $("#lord-battle-mastery .battle-mastery select").each(function() {
            var a = $(this).data("stat"),
                e = $(this).data("valperlevel"),
                i = $(this).val(),
                s = i * e,
                n = $(this).data("condition");
            checkCondition(n, l) && 0 != i && (t[a] = t[a] + parseFloat(s) || parseFloat(s))
        }), $("#equip-stats .equip").each(function() {
            var a = $(this),
                e = $(a).find(".set select").val(),
                i = $(a).find(".stuff select").val(),
                o = $(a).find(".enhancement select").val(),
                l = $(a).find(".item-rarity select").val();
            "" != e && (s[e] = s[e] + 1 || 1, n[e] = void 0 != n[e] ? n[e] + ";" + i : i), "" != i && "" != o && "" != l && (r += 1), $(a).find(".stat").each(function() {
                var a = $(this).data("stat"),
                    e = parseFloat($(this).data("val")) || 0;
                t[a] = t[a] + e || e
            })
        });
        var u = calculateEquipBonus(r);
        t.attack += u, $("#equip-attack-bonus").text(u), $("#equip-stats .potential").each(function() {
            var a = $(this).find(".potential-stat select").val(),
                e = $(this).find(".potential-val select").val() || 0;
            "" != a && 0 != e && (t[a] = t[a] + parseFloat(e) || parseFloat(e))
        });
        var p = $("#equip-stats .sets-activated");
        $(p).empty();
        for (var f in s) {
            var h = $("#sets-list .set-info[data-id='" + f + "']"),
                v = ($(h).data("title"), $(h).data("grade"), $(h).data("rank"), $(h).data("condition_label"), $(h).data("condition") || ""),
                m = $(h).clone();
            $(m).removeClass("active").attr("style", ""), $(m).find(".equips .icon, .effect").addClass("lighten");
            var g = n[f].split(";");
            for (var y in g) $(m).find(".icon[data-stuff='" + g[y] + "']").removeClass("lighten");
            var b = checkCondition(v, l);
            $(m).find(".effect-stat.effect2").each(function() {
                var e = $(this).closest(".set-info"),
                    i = ($(this).data("label"), $(this).data("stat")),
                    n = $(this).data("value"),
                    o = $(this).data("max") || "",
                    d = $(this).data("condition") || "";
                s[f] >= 2 && "" != d && checkCondition(d, l) && b ? ("" != o && (n = o), void 0 == t[i] && (t[i] = 0), a[i] = a[i] + parseFloat(n) || parseFloat(n), $(e).find(".effect.effect2").removeClass("lighten")) : s[f] >= 2 && "" == d && b ? (void 0 == t[i] && (t[i] = 0), a[i] = a[i] + parseFloat(n) || parseFloat(n), $(e).find(".effect.effect2").removeClass("lighten")) : b || $(e).find(".condition").addClass("text-red")
            }), $(m).find(".effect-stat.effect3").each(function() {
                var e = $(this).closest(".set-info"),
                    i = ($(this).data("label"), $(this).data("stat")),
                    n = $(this).data("value"),
                    o = $(this).data("max") || "",
                    d = $(this).data("condition") || "";
                3 == s[f] && "" != d && checkCondition(d, l) && b ? ("" != o && (n = o), void 0 == t[i] && (t[i] = 0), a[i] = a[i] + parseFloat(n) || parseFloat(n), $(e).find(".effect.effect3").removeClass("lighten")) : 3 == s[f] && "" == d && b && (void 0 == t[i] && (t[i] = 0), a[i] = a[i] + parseFloat(n) || parseFloat(n), $(e).find(".effect.effect3").removeClass("lighten"))
            }), $(p).append(m)
        }
        var S = sortByKey(arrayClone(t));
        removeAdditionalStatDisplayed(), checkStatsTableDisplay();
        var C = 0;
        $("#hero-stats #hero-stats-details #stats-table .stat:not(.stat-add)").each(function() {
            var s = $(this).data("stat"),
                n = $(this).data("multiplicative") || 0,
                o = $("#hero-" + tdf(s)).val() || 0,
                l = a[s] || 0,
                d = a[s + "%"] || 0,
                r = t[s] || 0,
                u = t[s + "%"] || 0,
                p = r + l,
                f = u + d;
            "criticaldamage" == s && (o = c), $(this).find(".base").text(o), $(this).find(".flat").text(roundIfFloat(p)), $(this).find(".pct").text(roundIfFloat(f)), $(this).find(".conversion").text("-"), n ? (e[s] = parseInt(p * (1 + f / 100)), i[s] = e[s], "defense" == s ? (C = defFormulaToPct(e[s]) + t[s + "!"] || defFormulaToPct(e[s]), defflat = defFormulaToFlat(C), i[s] = Math.round(defflat), $(this).find(".total").text(Math.round(defflat) + " (" + roundIfFloat(C) + " %)")) : $(this).find(".total").text("dodge" == s ? e[s] + " (" + roundIfFloat(dodgeFormulaToPct(e[s])) + " %)" : "critrate" == s || "hitrate" == s || "mastery" == s || "counterrate" == s || "counterdamage" == s ? e[s] + " (" + roundIfFloat(e[s] / 100) + " %)" : e[s])) : "criticaldamage" == s ? (i[s] = o + f, $(this).find(".total").text(roundIfFloat(i[s]) + " %")) : "movement" == s || "mprecovery" == s ? $(this).find(".total").text(p) : "dot" == s && $(this).find(".total").text(roundIfFloat(p) + " %"), void 0 != S[s] && delete S[s], void 0 != S[s + "%"] && delete S[s + "%"], void 0 != S[s + "!"] && delete S[s + "!"]
        });
        for (var d in S) {
            $row = createAdditionalStatDisplay(d);
            var q = a[d] || 0,
                k = t[d] || 0;
            i[d] = k + q, $($row).find(".base").text("-"), $($row).find(".flat").text("-"), $($row).find(".pct").text("-"), $($row).find(".conversion").text("-"), $($row).find(".total").text(roundIfFloat(i[d]))
        }
        var P = new Array;
        for (var d in t) - 1 != d.indexOf("by") && P.push(d);
        var x = new Array;
        for (var w in P) {
            var F = P[w],
                _ = F.split("by"),
                d = _[0],
                I = _[1],
                O = 0,
                E = t[I],
                N = t[I + "%"] || 0,
                A = parseInt(E * (1 + N / 100));
            "defense" == I ? (C = defFormulaToPct(A), O = Math.round(100 * C * (t[d + "by" + I] / 100))) : O = Math.round(A * (t[d + "by" + I] / 100)), x[d] = x[d] + O || O, i[d] = e[d] + x[d];
            var j = $("#hero-stats #hero-stats-details #stats-table .stat[data-stat='" + tdf(d) + "']");
            $(j).find(".total").text("dodge" == d ? i[d] + " (" + roundIfFloat(dodgeFormulaToPct(i[d])) + " %)" : "critrate" == d || "hitrate" == d || "mastery" == d || "counterrate" == d || "counterdamage" == d ? i[d] + " (" + roundIfFloat(i[d] / 100) + " %)" : i[d]), $(j).find(".conversion").text(x[d])
        }
        return data_compare.checkBuild() && data_compare.compareStats(i), i
    }
}

function toJSONpls() {
    var t = new Object;
    return data = $("form#calc-form").serializeArray(), $.each(data, function(a, e) {
        "" != e.value && (t[e.name] = e.value)
    }), t.lordcostumes = new Array, $("#lord-costumes .costume.active").each(function() {
        var a = $(this).data("id");
        t.lordcostumes.push(a)
    }), t.herocostumes = {}, $("#hero-costumes .costume.active").each(function() {
        var a = $(this).data("hero"),
            e = $(this).data("id");
        void 0 === t.herocostumes[a] && (t.herocostumes[a] = new Array), t.herocostumes[a].push(e)
    }), t.herosoulgears = {}, $("#hero-soul-gears .costume.active").each(function() {
        var a = $(this).data("hero"),
            e = $(this).data("type"),
            i = $(this).data("num");
        void 0 === t.herosoulgears[a] && (t.herosoulgears[a] = new Array), void 0 === t.herosoulgears[a][i] && (t.herosoulgears[a][i] = new Array), t.herosoulgears[a][i].push(e)
    }), json = JSON.stringify(t)
}

function saveJSONpls() {
    datajson = toJSONpls(), $.ajax({
        method: "POST",
        url: "ajax.save-stats.php",
        data: {
            dataform: datajson
        }
    }).done(function(t) {
        var a = JSON.parse(t);
        a.success ? buildNotification("success", a.message, void 0, 1) : buildNotification("danger", a.message, void 0, 1)
    })
}

function saveInSession() {
    datajson = toJSONpls(), $.ajax({
        method: "POST",
        url: "ajax.save-calc-session.php",
        data: {
            dataform: datajson
        }
    })
}

function loadJSONpls(t) {
    t = void 0 == t || "" == t ? 1 : t, loader.init(), $.ajax({
        method: "POST",
        url: "ajax.load-stats.php"
    }).done(function(a) {
        var e = JSON.parse(a);
        e.success ? (loadCalcFromJSON(e.data), t && buildNotification("success", e.message, void 0, 1)) : t && buildNotification("danger", e.message, void 0, 1)
    }), loader.stop()
}

function populateFields(t) {
    $("#calc-form")[0].reset(), $(".costume.active").removeClass("active"), data = JSON.parse(t);
    for (var a in data)
        if ("lordcostumes" == a) {
            if (0 != data[a].length)
                for (var e in data[a]) $("#lord-costumes div[data-id='" + data[a][e] + "']").addClass("active")
        } else if ("herocostumes" == a) {
        if (0 != data[a].length)
            for (var i in data[a])
                for (var e in data[a][i]) $("#hero-costumes ." + i + " div[data-id='" + data[a][i][e] + "']").addClass("active")
    } else if ("herosoulgears" == a) {
        if (0 != data[a].length)
            for (var i in data[a])
                for (var s in data[a][i])
                    for (var n in data[a][i][s]) $("#hero-soul-gears ." + i + " div[data-type='" + data[a][i][s][n] + "']").addClass("active")
    } else $("input[name='" + a + "'], select[name='" + a + "']").val(data[a])
}

function calculateEquipBonus(t) {
    var a = new Array(0, 10, 20, 30, 45, 60, 75, 95, 115, 135, 160, 185, 210, 240, 270, 300);
    return a[t]
}

function checkCondition(t, a) {
    {
        var e = !0;
        $("#button-ig")
    }
    return "" != t && (-1 != t.indexOf("=!") ? (condition_part = t.split("=!"), e = $(a).data(condition_part[0]) != condition_part[1] ? !0 : !1) : -1 != t.indexOf("=") ? (condition_part = t.split("="), e = $(a).data(condition_part[0]) == condition_part[1] ? !0 : !1) : e = "IG" == t && $("#button-ig").hasClass("bg-rare") ? !0 : !1), e
}

function removeAdditionalStatDisplayed() {
    $("#hero-stats #hero-stats-details .stat-add").remove()
}

function createAdditionalStatDisplay(a, e) {
    e = void 0 == e || "" == e ? 0 : e;
    var i = $("<tr>").addClass("stat stat-add");
    return $(i).data("stat", tdf(a)), $(i).data("multiplicative", e), $(i).append("<td>" + t(a) + "</td>"), $(i).append("<td class='base' style='display:none;'></td>"), $(i).append("<td class='flat' style='display:none;'></td>"), $(i).append("<td class='pct' style='display:none;'></td>"), $(i).append("<td class='conversion' style='display:none;'></td>"), $(i).append("<td class='total'></td>"), $("#hero-stats #stats-table tbody").append(i), i
}

function checkStatsTableDisplay() {
    var t = $("#hero-stats-details #stats-table"),
        a = $("#hero-stats-details #comparison");
    switch ($("#hero-stats-details .display-mode button.active").prop("id")) {
        case "stats-simple-overview":
            $(t).find(".base, .flat, .pct, .conversion").hide(), $(a).hide(), $(t).show();
            break;
        case "stats-detailed-overview":
            $(t).find(".base, .flat, .pct, .conversion").show(), $(a).hide(), $(t).show();
            break;
        case "stats-comparison":
            $(a).show(), $(t).hide()
    }
}

function roundIfFloat(t) {
    return Number.isInteger(t) || (t = t.toFixed(2)), t
}

function defFormulaToPct(t) {
    return val = .95 * t / (t + 6200) * 100
}

function dodgeFormulaToPct(t) {
    return val = .95 * t / (t + 7e3) * 100
}

function defFormulaToFlat(t) {
    return val = -6200 * t / (t - 95)
}

function tdf(t) {
    return t = t.toLowerCase(), t = t.replace(/ /g, "")
}

function arrayClone(t) {
    var a, e, i;
    a = Array.isArray(t) ? [] : {};
    for (i in t) e = t[i], a[i] = "object" == typeof e ? copy(e) : e;
    return a
}

function ucfirst(t) {
    return t.charAt(0).toUpperCase() + t.slice(1)
}

function sortByKey(t) {
    var a = Object.keys(t),
        e = a.length;
    a.sort();
    var s = {};
    for (i = 0; e > i; i++) k = a[i], s[k] = t[k];
    return s
}
window.onbeforeunload = function() {
    return saveInSession(), "No unsaved changes ?"
}, $.expr[":"].contains = $.expr.createPseudo(function(t) {
    return function(a) {
        return $(a).text().toUpperCase().indexOf(t.toUpperCase()) >= 0
    }
});
var stats_translation = {},
    current_language = "en";
$.ajax({
    method: "POST",
    url: "data.stats.php",
    data: {
        action: "getTranslation"
    }
}).done(function(t) {
    stats_translation = JSON.parse(t)
});
var data_compare = {
    json: "",
    stats: {},
    active: !1,
    button_save: $("#build-save"),
    button_restore: $("#build-restore"),
    button_delete: $("#build-delete"),
    saveBuild: function() {
        (!this.checkBuild() || confirm("A build is already saved, do you want to overwrite it ?")) && (this.active = !0, this.json = toJSONpls(), this.stats = arrayClone(calculatePls()), this.compareStats(this.stats), $(this.button_save).addClass("bg-rare"), $(this.button_restore).removeClass("disabled"), $(this.button_delete).removeClass("disabled"))
    },
    restoreBuild: function() {
        loader.init(), loadCalcFromJSON(this.json), loader.stop()
    },
    deleteBuild: function() {
        this.active = !1, this.json = "", this.stats = [], this.emptyDisplay(), $(this.button_save).removeClass("bg-rare"), $(this.button_restore).addClass("disabled"), $(this.button_delete).addClass("disabled")
    },
    compareStats: function(t) {
        if (!this.checkBuild()) return void alert("save stats first");
        this.emptyDisplay();
        var a = this.getAllStatsName(t);
        this.createStatsDisplay(a, t)
    },
    checkBuild: function() {
        return this.active
    },
    getAllStatsName: function(t) {
        stats_name = [];
        for (var a in t) stats_name[a] = !0;
        for (var a in this.stats) stats_name[a] = !0;
        return stats_name
    },
    emptyDisplay: function() {
        $("#hero-stats #comparison-table tbody").empty()
    },
    createStatsDisplay: function(a, e) {
        var s = $("#hero-stats #comparison-table tbody");
        i = 0;
        for (var n in a) {
            i++;
            var o = this.stats[n] || 0,
                l = e[n] || 0,
                d = $("<tr>").addClass("stat").data("stat", tdf(n)),
                r = $("<td>").text(t(n)),
                c = $("<td>").addClass("total1").text(roundIfFloat(o)),
                u = $("<td>").addClass("total2").text(roundIfFloat(l));
            i > 10 && d.addClass("stat-add"), o > l ? ($(c).addClass("text-green"), $(u).addClass("text-red")) : l > o && ($(c).addClass("text-red"), $(u).addClass("text-green")), $(d).append(r, c, u), $(s).append(d)
        }
    }
};
$(document).ready(function() {
    $('[data-toggle="tooltip"]').tooltip({
        container: "body"
    }), $("body").on("click", ".costume", function() {
        $(this).toggleClass("active"), calculatePls()
    }).on("change", "select.rarity", function() {
        applyBgRarity(this)
    }).on("change", "#hero-pick #select-hero", function() {
        displayIllustration(), displayCostumes(), displaySoulGears()
    }).on("click", "#hero-pick #apply-stats", function() {
        var t = ($("#select-hero").val(), $("#select-hero option:selected")),
            a = $(t).data();
        for (var e in a) $("#hero-stats #hero-" + tdf(e)).length && $("#hero-stats #hero-" + tdf(e)).val(a[e]);
        calculatePls()
    }).on("click", "#hero-pick #type-stats", function() {
        $("#hero-stats-type").toggle()
    }).on("click", "#hero-stats #apply-typed-stats", function() {
        $("#hero-stats-type .stat").each(function() {
            var t = $(this).data("stat"),
                a = parseInt($(this).find(".white-stat").val()) || 0,
                e = parseInt($(this).find(".red-stat").val()) || 0,
                i = a - e;
            $("#hero-stats-details #hero-" + tdf(t)).val(i)
        }), $("#hero-stats-type").hide(), calculatePls()
    }).on("change", "#hero-potentials .potential-stat select", function() {
        var t = $(this).closest(".potential").data("num");
        displayHeroPotential(t)
    }).on("change", "#equip-stats .set select", function() {
        getSetStuff(this)
    }).on("change", "#equip-stats .stuff select, #equip-stats .item-rarity select, #equip-stats .enhancement select, #equip-stats .set select", function() {
        loader.init(), updateItemSelects(this), $.when(getEquipStats(this)).done(function() {
            calculatePls(), loader.stop()
        })
    }).on("change", "#equip-stats .potential-stat select", function() {
        loader.init();
        var t = $(this).val();
        "" == t && $(this).attr("class", "form-control"), addCloneButton(this), updateEquipPotential(this), $.when(getEquipPotentials(this)).done(function() {
            calculatePls(), loader.stop()
        })
    }).on("click", "#equip-stats .action-clone-potential", function() {
        cloneEquipPotential(this)
    }).on("change", "#hero-potentials select, #lord-battle-mastery select, #hero-stats-damage input, #equip-stats .potential-val select", function() {
        calculatePls()
    }).on("click", "#group-atk #advantages #advantage, #group-atk #advantages #opposite-advantage", function() {
        $(this).is(":checked") && ("advantage" == $(this).attr("id") ? $("#opposite-advantage").removeAttr("checked") : $("#advantage").removeAttr("checked"))
    }).on("click", "#group-atk #advantages input", function() {
        calculatePls()
    }).on("click", ".platinum img", function() {
        togglePlatinum(this), updateItemSelects(this), getEquipStats(this), calculatePls()
    }).on("click", "#hero-stats-details .display-mode button", function() {
        toggleStatsTable(this)
    }).on("click", "#calc-save", function() {
        saveJSONpls()
    }).on("click", "#calc-load", function() {
        loadJSONpls()
    }).on("click", "#calc-export", function() {
        openExportDialog()
    }).on("click", "#calc-import", function() {
        openImportDialog()
    }).on("click", "#calc-json-textarea", function() {
        this.select()
    }).on("click", "#equip-btn-set button", function() {
        var t = $(this).data("role"),
            a = $(this).data("type");
        "legendary_max" == t ? (setEquipRarity("legendary"), setEnhancement(10)) : "transcended_max" == t ? (setEquipRarity("transcended"), setEnhancement(12), setEnhancement(13)) : "potential_common_build" == t ? (data = {}, data.weapon = ["attack%", "critrate%", "criticaldamage%", "damage%"], data.armor = ["hp%", "defense%", "damagetaken%", "dodge%"], data.accessory = ["attackbyhp", "hp%", "critrate%", "criticaldamage%", "damagetaken%", "boss%", "attack%", "defense%", "dodge%"], setItemPotentialsBuild(data, 1)) : "potential_max_common_build" == t ? (data = {}, data.weapon = ["attack%", "critrate%", "criticaldamage%", "damage%"], data.armor = ["hp%", "defense%", "damagetaken%", "dodge%"], data.accessory = ["attackbyhp", "hp%", "critrate%", "criticaldamage%", "damagetaken%", "boss%", "attack%", "defense%", "dodge%"], setItemPotentialsBuild(data, 0)) : "costumes" == t ? ($("#hero-costumes .costume:visible").addClass("active"), $("#lord-costumes .costume:visible").addClass("active"), $("#hero-soul-gears .costume:visible").addClass("active"), calculatePls()) : "platinum" == t ? setPlatinum(1) : "reset_equips" == t ? (resetEquips(), resetPotentials()) : "reset_potentials" == t ? resetPotentials() : setEquipStuff(a, t)
    }).on("click", ".btn-sets-list", function() {
        var t = $("#modal-sets");
        $(t).modal("show")
    }).on("click", "#btn-calc-import", function() {
        json = $("#calc-json-textarea").val(), "" != json && (loadCalcFromJSON(json), $("#modal-calc").modal("hide"))
    }).on("keyup", "#sets-filter input", function() {
        filterSets()
    }).on("click", "#sets-filter button[data-role='filter']", function() {
        var t = $(this);
        t.hasClass("active") ? t.removeClass("active") : ($(this).closest(".btn-group").find("button").removeClass("active"), t.addClass("active")), filterSets()
    }).on("click", "#sets-filter button[data-role='reset']", function() {
        $("#sets-filter button[data-role='filter']").removeClass("active"), $("#sets-filter input").val(""), filterSets()
    }).on("click", ".div-close", function() {
        $(this).parent().toggle()
    }).on("click", "#sets-list .set-info", function() {
        if (confirm("Do you want to equip this set ?")) {
            $(this).closest(".sets-grade").find(".set-info").removeClass("active"), $(this).addClass("active");
            var t = $(this).data("grade"),
                a = $(this).data("id"),
                e = $(".equip[data-grade='" + t + "']");
            setSet(e, a)
        }
    }).on("click", "button#button-ig", function() {
        $(this).toggleClass("bg-rare").toggleClass("btn-default"), calculatePls()
    }).on("click", ".left-bloc .switch", function() {
        var t = $(this).parent();
        $(t).toggleClass("left-hidden"), $(".mid-bloc").toggleClass("left-hidden"), $(this).find("span").toggleClass("glyphicon-triangle-right"), $(this).find("span").toggleClass("glyphicon-triangle-left")
    }).on("click", ".right-bloc .switch", function() {
        var t = $(this).parent();
        $(t).toggleClass("right-hidden"), $(".mid-bloc").toggleClass("right-hidden"), $(this).find("span").toggleClass("glyphicon-triangle-right"), $(this).find("span").toggleClass("glyphicon-triangle-left")
    }).on("click", "#build-save", function() {
        data_compare.saveBuild()
    }).on("click", "#build-restore", function() {
        data_compare.restoreBuild()
    }).on("click", "#build-delete", function() {
        data_compare.deleteBuild()
    })
});
var timeout_list = [],
    loader = {
        init: function() {
            timeout = setTimeout(function() {
                $(".loader").fadeIn(300)
            }, 1e3), timeout_list.push(timeout)
        },
        stop: function() {
            for (var t in timeout_list) clearTimeout(timeout_list[t]);
            $(".loader").fadeOut(300)
        }
    };
