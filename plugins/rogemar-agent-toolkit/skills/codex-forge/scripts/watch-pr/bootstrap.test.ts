import {it,expect} from 'bun:test';
import {mkdtemp,copyFile,writeFile,readdir,rm} from 'node:fs/promises';
import {join} from 'node:path';
import {tmpdir} from 'node:os';
it('a dependency diagnostic does not install packages or create markers',async()=>{
 const dir=await mkdtemp(join(tmpdir(),'forge diagnostic '));
 try {
  await copyFile(join(import.meta.dir,'../bootstrap.ts'),join(dir,'bootstrap.ts'));
  await writeFile(join(dir,'package.json'),JSON.stringify({dependencies:{commander:'14.0.0'}}));
  await writeFile(join(dir,'probe.ts'),"import {ensureDependenciesInstalled} from './bootstrap.ts'; ensureDependenciesInstalled();");
  const before=await readdir(dir);const p=Bun.spawn([process.execPath,join(dir,'probe.ts')],{stdout:'pipe',stderr:'pipe'});
  expect(await p.exited).not.toBe(0);expect(await new Response(p.stderr).text()).toContain('did not install anything');
  expect(await readdir(dir)).toEqual(before);
 } finally {await rm(dir,{recursive:true,force:true});}
});
