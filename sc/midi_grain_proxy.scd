s.options.memSize_(32768);
s.options.numAudioBusChannels_(3072);
s.boot;
(

SynthDef(\grain, {|out=0,freq=200,amp=0.1,grain_dur=0.01,pos=0|
	var sig = FSinOsc.ar(freq) * amp * EnvGen.ar(Env.sine(grain_dur),doneAction:2);
	OffsetOut.ar(out,Pan2.ar(sig,pos));
}).add;

SynthDef(\cloud_env_nonfixed,{|out=0,inbus,gate=0,atk=0.1,sus_lvl=1,rel=1|
	var env = Env.asr(atk,sus_lvl,rel); // 4 stage adsr fixed length
	Out.ar(out, In.ar(inbus, 2) * EnvGen.ar(env,gate,doneAction:2)); // Julian's fix... In.ar(inbus)
}).add;


p = ProxySpace.push.fadeTime_(1);
f = Environment.new().know_(true);
e = (            // this is the event that updates SCsynth
	\rel:1,
	\amp: 0.5,

	\freq: 540,
	\freq_dev: 0,
	\grain_rate:0.1, // dur in Pbind
	\grain_rate_dev: 0,
	\grain_dur: 0.01,
	\grain_dur_dev: 0,

	\n_voices: 1,
);

h = (                   // this gets updated with midi values... saves reconversion
	\id: 0,

	\rel:0,
	\amp: 0,
	\freq: 0,
	\freq_dev: 0,
	\grain_rate:0, // dur in Pbind
	\grain_rate_dev: 0,
	\grain_dur: 0,
	\grain_dur_dev: 0,
	\n_voices: 0,

	\noteOn_timestamp: 0,
	\noteOff_timestamp:0
);


)

(
g = (
	i: 0,
	pattern_buff: Array.newClear(128),
	cloud_buff: Array.newClear(128),
	temp_buff: Array.newClear(128),
	output_dict: Dictionary()
); // global buffers
)


( // cloud generator -- helper function that reads from global event
f.cloud_maker = {

	var grain_rate_dev = e.grain_rate * e.grain_rate_dev;
	var freq_dev = e.freq * e.freq_dev;
	var grain_dur_dev = e.grain_dur * e.grain_dur_dev;

	~pattern=nil;
	e.n_voices.do({|i|
		~pattern[i] = Pbind(
			\instrument,\grain,
			\dur, Pexprand(e.grain_rate-grain_rate_dev, e.grain_rate + grain_rate_dev),
			\freq, Pexprand(e.freq-freq_dev, e.freq + freq_dev),
			\amp, Pwhite(0.01,e.amp),
			\grain_dur, Pexprand(e.grain_dur-grain_dur_dev, e.grain_dur + grain_dur_dev),
			\pos, Pwhite(-1,1)
		);
	});
	~pattern;
};
)

(
MIDIClient.init;
MIDIIn.connectAll;
)

//verb -- just for fun... do not track values
//~out.play;
//~out.stop;
//~out = nil
//~out = {FreeVerb.ar(g.pattern_buff[nn].ar,0.7,0.75,0.45)};

(
MIDIdef.noteOn(\noteOnTest, { |vel,nn|

	[vel,nn].postln;
	h.freq = nn;   // store current note midi
	e.freq = nn.midicps;  //
	g.pattern_buff[nn] = f.cloud_maker.().copy.play;


	h.noteOn_timestamp = Clock.seconds; // add the current timestep
	h.id = g.i;                    // add current increment
	g.temp_buff[nn] = h;            // copy into temp_buff to wait for noteOff
	g.i = g.i + 1;

}).permanent_(true);

MIDIdef.noteOff(\noteOffTest, {|vel,nn|
	[vel,nn].postln;
	// free up resources
	g.pattern_buff[nn].free(e.rel);
	g.pattern_buff[nn] = nil;

	~pattern.free;
	//~pattern.end;
	// finish loading data into dictionary
	g.temp_buff[nn].noteOff_timestamp = Clock.seconds;
	g.output_dict.add(g.temp_buff[nn].id -> g.temp_buff[nn].deepCopy);
	g.temp_buff[nn] = nil;


}).permanent_(true);


// one cc for each knob, 8 total
// these set the values for global ~event for the next noteOn
MIDIdef.cc(\ccAmp,{|value, cc_num|
	h.amp = value;
	e.amp = value.linexp(0,127,0.01,1);
	postln("Amp: "++ e.amp);
},21).permanent_(true);

MIDIdef.cc(\ccRel,{|value, cc_num|
	h.rel = value;
	e.rel = value.linexp(0,127,0.3,5);
	postln("Release: "++ e.rel);
},22).permanent_(true);

MIDIdef.cc(\ccnVoices,{|value, cc_num|
	h.n_voices = value;
	e.n_voices = value.linlin(0,127,1,5).round;
	postln("N_Voices: "++ e.n_voices);
},23).permanent_(true);

MIDIdef.cc(\ccFreqDev,{|value, cc_num|
	h.freq_dev = value;
	e.freq_dev = value.linlin(0,127,0,0.99);
	postln("Freq_Deviation: "++ e.freq_dev);
},24).permanent_(true);

MIDIdef.cc(\ccGrainRate,{|value, cc_num|
	h.grain_rate = value;
	e.grain_rate = value.linexp(0,127,0.01,1);
	postln("Grain Rate: "++ e.grain_rate);
},25).permanent_(true);

MIDIdef.cc(\ccGrainRateDev,{|value, cc_num|
	h.grain_rate_dev = value;
	e.grain_rate_dev = value.linlin(0,127,0,0.99);
	postln("Grain Rate Deviation: "++ e.grain_rate_dev);
},26).permanent_(true);

MIDIdef.cc(\ccGrainDur,{|value, cc_num|
	h.grain_dur = value;
	e.grain_dur = value.linexp(0,127,0.01,0.1);
	postln("Grain Dur: "++ e.grain_dur);
},27).permanent_(true);

MIDIdef.cc(\ccGrainDurDev,{|value, cc_num|
	h.grain_dur_dev = value;
	e.grain_dur_dev = value.linlin(0,127,0,0.99);
	postln("Grain Dur Deviation: "++ e.grain_dur_dev);
},28).permanent_(true);

)

// noteOn ... add TimeStap and id; copy current h into temp array[nn] to wait for noteOff
// noteOff ... add TimeStamp; add array to output Dict.. key equals id number
//


//JSON export
File.use("grain_improv3.json".resolveRelative,"w",{|f| f.write(JSON.stringify(g.output_dict))});
