import asyncio,shlex,os,logging,time
from typing import Union,Optional,List,Tuple

# ref https://info.nrao.edu/computing/guide/file-access-and-archiving/7zip/7z-7za-command-line-guide
torlog = logging.getLogger(__name__)

async def cli_call(cmd: Union[str,List[str]]) -> Tuple[str,str]:
    if isinstance(cmd,str):
        cmd = shlex.split(cmd)
    elif isinstance(cmd,(list,tuple)):
        pass
    else:
        return None,None
    
    process = await asyncio.create_subprocess_exec(
        *cmd,
        stderr=asyncio.subprocess.PIPE,
        stdout=asyncio.subprocess.PIPE
    )

    stdout, stderr = await process.communicate()
    
    stdout = stdout.decode().strip()
    stderr = stderr.decode().strip()
    
    return stdout, stderr

async def split_in_zip(path):
    if os.path.exists(path):
        if os.path.isfile(path):
            fname = os.path.basename(path)
            bdir = os.path.dirname(path)
            bdir = os.path.join(bdir,str(time.time()).replace(".",""))
            if not os.path.exists(bdir):
                os.mkdir(bdir)

            cmd = f"7z a -tzip '{bdir}/{fname}.zip' '{path}' -v1900m "

            out, err = await cli_call(cmd)
            
            if err:
                torlog.error(f"Error in zip split {err}")
                return None
            else:
                return bdir

                
        else:
            return None
    else:
        return None