on("ready", function() {
	if (!state.MainGameNS) {
		state.MainGameNS = { GameTime: 0 };
	}
	log("go")

	//log(out)
	//if (trace) { log(`API table : ${JSON.stringify(tables,null,4)}`) }
});

on("chat:message", function(msg) {

	if (msg.type == "api") {
		var args = msg.content.split(" ");
		if (args[0] == "!out") {
		    char_out(msg);
		} else 
		if (args[0] == "!allout") {
		    char_out_all(msg);
		}
	}
});
function isInt(str) {
  if (typeof str != "string") return false // we only process strings!  
  return !isNaN(str) && // use type coercion to parse the _entirety_ of the string (`parseFloat` alone does not do this)...
         !isNaN(parseInt(str)) // ...and ensure strings of whitespace fail
}
const getGMPlayers = (pageid) => findObjs({ type: 'player' })
	.filter((p) => playerIsGM(p.id))
	.filter((p) => undefined === pageid || p.get('lastpage') === pageid)
	.map(p => p.id)
	;

const sendGMPing = (left, top, pageid, playerid = null, moveAll = false) => {
	let players = getGMPlayers(pageid);
	if (players.length) {
		sendPing(left, top, pageid, playerid, moveAll, players);
	}
};


function char_out(msg) {
    
	if (!msg.selected) { return; }
	//log(msg.selected);
	var objid = msg.selected[0];
	log(objid['_id']);
	var toke = getObj("graphic", objid['_id']);
	sendGMPing(toke.get('left'), toke.get('top'), toke.get('pageid'), "", true);
	sendChat("Out Character", "/w gm " + toke.get('name'));

	
	var atts = findObjs({
		_characterid: toke.get('represents'),
		_type: "attribute",

	});
	var loki = findObjs({
		_characterid: toke.get('represents'),
		_type: "attribute",
		name: "pb",

	});
	var sheettype = findObjs({
		_characterid: toke.get('represents'),
		_type: "attribute",
		name: "charactersheet_type",

	})[0];
	//log(atts)
	var out = tables;


	log("start.........................................")
	_.each(atts, function(obj) {
        var n = obj.get('name')
        var val = obj.get('current');
        if (isInt(val)) {
            val = parseInt(val)
        }

        if (!String(val).startsWith('@{w')) { 

            if (String(n).includes("kingdom_drop_data")) {
                out[n] = JSON.parse(val);
            }
            if (n.endsWith('_prof')) {
                n = n + "icient";
                if (String(val).startsWith('(@{pb')) {
                    val = loki[0].get('current');
                } else {
                    val = 0;
                }
            }
            

            if (n.startsWith('repeating_')) {
                
                var ary = n.split("_")
                var c = ary[0].length + ary[1].length + ary[2].length +3;
                var t1 = {};
                t1[n.slice(c)] = val;
                if (ary[1]== 'inventory') {
                    if (n.slice(c) == 'useasresource') {
                        t1['worn'] = 1;
                        t1['value'] = 1;
                    } else {
                        t1['useasresource'] = 0;
                        t1['worn'] = 1;
                        t1['value'] = 1;
                    }

                }
                var t2 = {}
                t2[ary[2]] = t1;
                if (ary[1] in out) {
                    if (ary[2] in out[ary[1]]) {
                        Object.assign(out[ary[1]][ary[2]],t1)
                    } else {
                        Object.assign(out[ary[1]], t2);
                    }
                    
                } else {
                    out[ary[1]] = t2;
                }
                
            } else {
                out[n] = val;
            } 
        }
        

	    
	});
	if ('pb' in out) {} else {
	    out['pb'] = 0;
	}
	out['hp_max'] = out['hp'];
	out['ac_desc'] = "ac desc";
	var tout = JSON.stringify(out,null,2)
	if (sheettype == "npc") {
    	var outbox = findObjs({
    		_characterid: toke.get('represents'),
    		_type: "attribute",
    		name: "npc_mythic_actions_desc",
    
    	});
    	outbox[0].set("current", tout)
	} else {
    	var outbox = findObjs({
    		_characterid: toke.get('represents'),
    		_type: "attribute",
    		name: "allies_and_organizations",
    
    	});
    	outbox[0].set("current", tout)	    
	}
}
function char_out_all(msg) {
    
	if (!msg.selected) { return; }
	//log(msg.selected);
	var objid = msg.selected[0];
	//log(objid['_id']);
	var toke = getObj("graphic", objid['_id']);
	sendGMPing(toke.get('left'), toke.get('top'), toke.get('pageid'), "", true);
	sendChat("Out Character", "/w gm " + toke.get('name'));

	var sheettype = findObjs({
		_characterid: toke.get('represents'),
		_type: "attribute",
		name: "charactersheet_type",

	})[0];
	//log(at
	var atts = findObjs({
		_characterid: toke.get('represents'),
		_type: "attribute",

	});
	//log(atts)
	var out = {};


	log("start...............all...................")
	_.each(atts, function(obj) {
        var n = obj.get('name')
        var val = obj.get('current');
        if (isInt(val)) {
            val = parseInt(val)
        }

        if (!String(val).startsWith('#@{w')) { 

            

            if (n.startsWith('repeating_')) {
                
                var ary = n.split("_")
                var c = ary[0].length + ary[1].length + ary[2].length +3;
                var t1 = {};
                t1[n.slice(c)] = val;

                var t2 = {}
                t2[ary[2]] = t1;
                if (ary[1] in out) {
                    if (ary[2] in out[ary[1]]) {
                        Object.assign(out[ary[1]][ary[2]],t1)
                    } else {
                        Object.assign(out[ary[1]], t2);
                    }
                    
                } else {
                    out[ary[1]] = t2;
                }
                
            } else {
                out[n] = val;
            } 
        }
        

	    
	});

	var tout = JSON.stringify(out,null,2)
	if (sheettype == "npc") {
    	var outbox = findObjs({
    		_characterid: toke.get('represents'),
    		_type: "attribute",
    		name: "npc_mythic_actions_desc",
    
    	});
    	outbox[0].set("current", tout)
	} else {
    	var outbox = findObjs({
    		_characterid: toke.get('represents'),
    		_type: "attribute",
    		name: "allies_and_organizations",
    
    	});
    	outbox[0].set("current", tout)	    
	}
}
