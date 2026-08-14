Import("env")

# Remove -Wl,-Map flag to fix non-ASCII Windows path issue in GCC ld
new_linkflags = []
for flag in env.get("LINKFLAGS", []):
    if isinstance(flag, str) and "-Map" in flag:
        continue
    new_linkflags.append(flag)
env.Replace(LINKFLAGS=new_linkflags)
