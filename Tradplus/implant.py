import os


def Run( projpath, dependsContent ):
    print(f'project path: {projpath}')
    print(f'depend content: {dependsContent}')

    if not projpath.endswith('mainTemplate.gradle'):
       projpath = os.path.join(projpath,'mainTemplate.gradle')

    filterstr = ''
    dependlines = dependsContent.splitlines()
    tradplusContent = False
    admob = False
    admob_bidding = False
    for l in dependlines:
        if l.startswith('dependencies {'):
            tradplusContent = True
        elif l.startswith('android {'):
            filterstr = filterstr[0:-2]
            break
        elif tradplusContent:
            real = l.replace('\"','\'')
            if admob:
                admob = False
                si = real.find('\'')
                ei = real.find('\'',si+1)
                com = real[si:ei+1]
                _import = '''    implementation(%s) {
        exclude module: "play-services-measurement-sdk-api"
    }\n'''%(com)
                filterstr += _import
                admob_bidding = True
                continue
            if admob_bidding and '// ' in real:
                _import = '''    //ADMOB BIDDING
    implementation ('com.applovin.mediation:google-adapter:22.1.0.0'){
        exclude module: "play-services-measurement-sdk-api"
    }\n'''
                filterstr += _import
                admob_bidding = False
            if '// Admob' in real:
                admob = True

            filterstr += f'{real}\n'


    output = ''
    with open(projpath,'r',encoding='UTF-8') as fp:
        begin_write = False
        lines = fp.readlines()
        for line in  lines:
            if line.startswith('    /////////////////////// TradPlus Start //////////////////////'):
                output += '    /////////////////////// TradPlus Start //////////////////////\n'
                output += filterstr
                begin_write = True
            elif line.startswith('    /////////////////////// TradPlus End //////////////////////'):
                output += '    /////////////////////// TradPlus End //////////////////////\n'
                begin_write = False
            elif not begin_write:
                output += line

    if len(output) != 0 and output != '':
        with open(projpath,'w',encoding='UTF-8') as fp:
            fp.write(output)

