// midi grain sketch
// event controlled cloud_env/grain pair using Ppar/Pbind/Pdef


//setup synthdefs and buses
(
SynthDef(\gauss_sine, {|out=0,freq=500,amp=0.1,grain_dur=0.01,pos=0|
	var sig = FSinOsc.ar(freq) * amp * EnvGen.ar(Env.sine(grain_dur),doneAction:2);
	OffsetOut.ar(out,Pan2.ar(sig,pos));
}).add;

SynthDef(\cloud_env_fixed,{|out=0,inbus,gate=1,sus_lvl=0.75,atk=0.1,dec=0.1,sus=1,rel=1|
	var env = Env([0.001,1,sus_lvl,sus_lvl,0.001],[atk,dec,sus,rel],\exp); // 4 stage adsr fixed length
	Out.ar(out, In.ar(inbus, 2) * EnvGen.ar(env,gate,doneAction:2)); // Julian's fix... In.ar(inbus)
}).add;

SynthDef(\cloud_env_nonfixed,{|out=0,inbus,gate=0,atk=0.1,dec=0.1,sus_lvl=1,rel=1|
	var env = Env.adsr(atk,dec,sus_lvl,rel); // 4 stage adsr fixed length
	Out.ar(out, In.ar(inbus, 2) * EnvGen.ar(env,gate,doneAction:2)); // Julian's fix... In.ar(inbus)
}).add;

~grain_bus = Bus.audio()
)

// globally scoped event to get parameters
// construct Pdef using settings (with Ppar for multiple voices)
// deviations must be between 0 and 0.99 since exprand is being used
(

~event = (\inbus: ~grain_bus.index,
	\atk:0.1,
	\rel:5,
	\vel: 0,

	\freq: 540,
	\freq_dev: 0,
	\grain_rate:0.1, // dur in Pbind
	\grain_rate_dev: 0,
	\grain_dur: 0.01,
	\grain_dur_dev: 0,

	\n_voices: 1,
	\noteOn_timestamp: 0,
	\noteOff_timestamp:0
)
)

(
~def = Array.newClear(128);
~cloud = Array.newClear(128);
//~output = Dictionary();
//~current_events = Array.newClear();  // current event gets copied here for noteoff and append reference
)

( // works with global event to build Pbinds for MIDI.noteOn()
~cloud_maker = {

	var coll;
	var grain_rate_dev = ~event.grain_rate * ~event.grain_rate_dev;
	var freq_dev = ~event.freq * ~event.freq_dev;
	var grain_dur_dev = ~event.grain_dur * ~event.grain_dur_dev;

	coll = Array.newClear(~event.n_voices);

	// make a collection of Pbinds one for each voice
	~event.n_voices.do({|i|
		coll[i] = Pbind(
			\instrument, \gauss_sine,
			\out, ~grain_bus.index,
			\dur, Pexprand(~event.grain_rate-grain_rate_dev, ~event.grain_rate + grain_rate_dev),
			\freq, Pexprand(~event.freq-freq_dev, ~event.freq + freq_dev),
			\amp, Pwhite(0.05,0.1),
			\grain_dur, Pexprand(~event.grain_dur-grain_dur_dev, ~event.grain_dur + grain_dur_dev),
			\pos, 0 //Pwhite(-1,1)
		);
	});
	coll;
}
)

// Midi

MIDIClient.init;
MIDIIn.connectAll;


(
MIDIdef.noteOn(\noteOnTest, { |vel,nn|
	var pbinds;

	[vel,nn].postln;
	//generate the cloud
	~event.freq = nn.midicps;

	pbinds = ~cloud_maker.();
	~def[nn] = Pdef(\p, Ppar(pbinds)).fork;
	~cloud[nn] = Synth(\cloud_env_nonfixed,[
		\gate,vel,
		\inbus,~event.inbus,
		\atk, ~event.atk,
		\rel,~event.rel,
		\sus_lvl, 0.75//0.25 * vel.linlin(0,127,0.1,0.75)
	]);


	// store these settings in previous event
	Clock.seconds;
}).permanent_(true);

MIDIdef.noteOff(\noteOffTest, {|vel,nn|
	[vel,nn].postln;
	// turn off cloud_env and  at given nn

	~def[nn].stop;
	~cloud[nn].set(\gate,0);
	/*Task({
		~cloud[nn].set(\gate,0);
		~event.rel.wait;
		~def[nn].stop;
		~cloud[nn] = nil;
		~def[nn] = nil;
	}).play;*/

	Clock.seconds;
}).permanent_(true);


// one cc for each knob, 8 total
// these set the values for global ~event for the next noteOn
MIDIdef.cc(\ccAtk,{|value, cc_num|
	~event.atk = value.linexp(0,127,0.5,1.5);
	postln("Attack: "++~event.atk);
},21).permanent_(true);

MIDIdef.cc(\ccRel,{|value, cc_num|
	~event.rel = value.linexp(0,127,0.3,5);
	postln("Release: "++~event.rel);
},22).permanent_(true);

MIDIdef.cc(\ccnVoices,{|value, cc_num|
	~event.n_voices = value.linlin(0,127,1,10).round;
	postln("N_Voices: "++~event.n_voices);
},23).permanent_(true);

MIDIdef.cc(\ccFreqDev,{|value, cc_num|
	~event.freq_dev = value.linlin(0,127,0,0.99);
	postln("Freq_Deviation: "++~event.freq_dev);
},24).permanent_(true);

MIDIdef.cc(\ccGrainRate,{|value, cc_num|
	~event.grain_rate = value.linexp(0,127,0.01,1);
	postln("Grain Rate: "++~event.grain_rate);
},25).permanent_(true);

MIDIdef.cc(\ccGrainRateDev,{|value, cc_num|
	~event.grain_rate_dev = value.linlin(0,127,0,0.99);
	postln("Grain Rate Deviation: "++ ~event.grain_rate_dev);
},26).permanent_(true);

MIDIdef.cc(\ccGrainDur,{|value, cc_num|
	~event.grain_dur = value.linexp(0,127,0.001,1);
	postln("Grain Dur: "++ ~event.grain_dur);
},27).permanent_(true);

MIDIdef.cc(\ccGrainDurDev,{|value, cc_num|
	~event.grain_dur_dev = value.linlin(0,127,0,0.99);
	postln("Grain Dur Deviation: "++~event.grain_dur_dev);
},28).permanent_(true);

)


~out = {FreeVerb.ar(~pattern.ar,)}
