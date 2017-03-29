(
p = ProxySpace.push;

~grain = {||
	GrainSin.ar(2,trig,graindur, 440 + freqdev,pan);
};


)


(
~def = Array.newClear(128);
~cloud = Array.newClear(128);

MIDIClient.init;
MIDIIn.connectAll;
)

(
MIDIdef.noteOn(\noteOnTest, { |vel,nn|
	var pbinds;

	[vel,nn].postln;
	//generate the cloud


	// store these settings in previous event
	Clock.seconds;
}).permanent_(true);

MIDIdef.noteOff(\noteOffTest, {|vel,nn|
	[vel,nn].postln;
	// turn off cloud_env and  at given nn

	Clock.seconds;
}).permanent_(true);


// one cc for each knob, 8 total
// these set the values for global ~event for the next noteOn
MIDIdef.cc(\ccAtk,{|value, cc_num|

},21).permanent_(true);

MIDIdef.cc(\ccRel,{|value, cc_num|

},22).permanent_(true);

MIDIdef.cc(\ccnVoices,{|value, cc_num|

},23).permanent_(true);

MIDIdef.cc(\ccFreqDev,{|value, cc_num|

},24).permanent_(true);

MIDIdef.cc(\ccGrainRate,{|value, cc_num|

},25).permanent_(true);

MIDIdef.cc(\ccGrainRateDev,{|value, cc_num|

},26).permanent_(true);

MIDIdef.cc(\ccGrainDur,{|value, cc_num|

},27).permanent_(true);

MIDIdef.cc(\ccGrainDurDev,{|value, cc_num|

},28).permanent_(true);

)

