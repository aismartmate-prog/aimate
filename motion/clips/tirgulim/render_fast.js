// Fast render: one frame per tick (no motion-blur subframes), a frame range per process so chunks run in parallel.
// NODE_PATH=motion/node_modules node render_fast.js page.html out.mp4 fps startFrame endFrame
const {chromium}=require('playwright');const {spawn}=require('child_process');const path=require('path');
(async()=>{const [html,out,fps,a,b]=process.argv.slice(2);const FPS=+fps,F0=+a;
 const br=await chromium.launch();const p=await br.newPage({viewport:{width:+(process.env.VW||1080),height:+(process.env.VH||1920)}});
 await p.goto('file://'+path.resolve(html)+'?render');await p.evaluate(()=>document.fonts.ready);await p.waitForTimeout(500);
 const N=Math.min(+b,Math.round(await p.evaluate(()=>window.DURATION)*FPS));
 const ff=spawn('ffmpeg',['-loglevel','error','-y','-f','image2pipe','-framerate',String(FPS),'-c:v','mjpeg','-i','-','-c:v','libx264','-crf','14','-preset','medium','-pix_fmt','yuv420p',out]);
 for(let f=F0;f<N;f++){await p.evaluate(t=>seek(t),f/FPS);const buf=await p.screenshot({type:'jpeg',quality:95});if(!ff.stdin.write(buf))await new Promise(r=>ff.stdin.once('drain',r));}
 ff.stdin.end();await new Promise(r=>ff.on('close',r));await br.close();console.log('chunk',F0,N,'done');})();
