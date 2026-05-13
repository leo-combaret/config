How to use our internal tools to profile and keep Zed fast.
# Rough quick CPU profiling (Flamechart)
See what the CPU spends the most time on. Strongly recommend you use samply . It opens an interactive profile in the browser (specifically a local instance of firefox_profiler ).
See samply 's README on how to install and run.
The profile.json does not contain any symbols. Firefox profiler can add the local symbols to the profile for for. To do that hit the upload local profile button in the top right corner.
# In depth CPU profiling (Tracing)
See how long each annotated function call took and its arguments (if configured).
Annotate any function you need appear in the profile with instrument. For more details see tracing-instrument :
```
#![allow(unused)]

fn main() {

#[instrument(skip_all)]
fn should_appear_in_profile(kitty: Cat) {
    sleep(QUITE_LONG)
}

}
```
Then either compile Zed with ZTRACING=1 cargo r --features tracy --release . The release build is optional but highly recommended as like every program Zeds performance characteristics change dramatically with optimizations. You do not want to chase slowdowns that do not exist in release.
## One time Setup/Building the profiler:
Download the profiler: linux x86_64 macos aarch64
### Alternative: Building it yourself
- Clone the repo at git@github.com:wolfpld/tracy.git
- cd profiler && mkdir build && cd build
- Run cmake to generate build files: cmake -G Ninja -DCMAKE_BUILD_TYPE=Release ..
- Build the profiler: ninja
- [Optional] move the profiler somewhere nice like ~/.local/bin on linux
## Usage
Open the profiler (tracy-profiler), you should see zed in the list of Discovered clients click it.
Tracy is an incredibly powerful profiler which can do a lot however it's UI is not that friendly. This is not the place for an in depth guide to Tracy, I do however want to highlight one particular workflow that is helpful when figuring out why a piece of code is sometimes slow.
Here are the steps:
1. Click the flamechart button at the top.
1. Click on a function that takes a lot of time.
1. Expand the list of function calls by clicking on main thread.
1. Filter that list to the slower calls then click on one of the slow calls in the list
1. Click zoom to zone to go to that specific function call in the timeline
1. Scroll to zoom in and see more detail about the callers
1. Click on a caller to to get statistics on it .
While normally the blue bars in the Tracy timeline correspond to function calls they can time any part of a codebase. In the example below we have added an extra span "for block in edits" and added metadata to it: the block_height. You can do that like this:
```
#![allow(unused)]

fn main() {

let span = ztracing::debug_span!("for block in edits", block_height = block.height());
let _enter = span.enter(); // span guard, when this is dropped the span ends (and its duration is recorded)

}
```
# Task/Async profiling
Get a profile of the zed foreground executor and background executors. Check if anything is blocking the foreground too long or taking too much (clock) time in the background.
The profiler always runs in the background. You can save a trace from its UI or look at the results live.
## Setup/Building the importer:
Download the importer linux x86_64 mac aarch64
### Alternative: Building it yourself
- Clone the repo at git@github.com:zed-industries/tracy.git on v0.12.2 branch
- cd import && mkdir build && cd build
- Run cmake to generate build files: cmake -G Ninja -DCMAKE_BUILD_TYPE=Release ..
- Build the importer: ninja
- Run the importer on the trace file: ./tracy-import-miniprofiler /path/to/trace.miniprof.json /path/to/output.tracy
- Open the trace in tracy: If you're on windows download the v0.12.2 version from the releases on the upstream repo If you're on other platforms open it on the website: https://tracy.nereid.pl/ (the version might mismatch so your luck might vary, we need to host our own ideally..)
## To Save a Trace:
- Run the action: zed open performance profiler
- Hit the save button. This opens a save dialog or if that fails to open the trace gets saved in your working directory.
- Convert the profile so it can be imported in tracy using the importer: ./tracy-import-miniprofiler <path to performance_profile.miniprof.json> output.tracy
- Go to https://tracy.nereid.pl/ hit the 'power button' in the top left and then open saved trace.
- Now zoom in to see the tasks and how long they took
# Warn if function is slow
```
#![allow(unused)]

fn main() {

let _timer = zlog::time!("my_function_name").warn_if_gt(std::time::Duration::from_millis(100));

}
```