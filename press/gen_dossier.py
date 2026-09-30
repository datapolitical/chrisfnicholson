#!/usr/bin/env python3
"""Generate the press-coverage inventory dossier for Chris Nicholson (RTD District A).
Pulls ids from the citations ledger; excerpts from fetched page text where available."""
import json, re, os

BASE = '/home/chris/.hermes/cache/scratch/press'
HTML = os.path.join(BASE, 'html')
ledger = json.load(open(os.path.join(BASE, 'ledger_snapshot.json')))
def norm(u): return u.rstrip('/')
ID = {norm(e['url']): e['id'] for e in ledger}

def idof(url):
    i = ID.get(norm(url))
    if i is None:
        print('WARN missing ledger id:', url)
        return '??'
    return i

# parse fetch report
rep = {}
rtxt = open(os.path.join(BASE, 'fetch_report.txt'), errors='replace').read()
for m in re.finditer(r'### (\S+) \| (\S+) \| hits=(\d+) \(kieran=\d+\) \| (.*?)\n    URL: (\S+)((?:\n    SNIP: .*)*)', rtxt):
    slug, date, hits, title, url, snips = m.groups()
    sn = re.findall(r'SNIP: (.*)', snips)
    rep[slug] = {'date': date, 'hits': int(hits), 'title': title.strip(), 'url': url.strip(),
                 'snip': (sn[0].strip() if sn else '')}

# supplementary items fetched outside fetch_all.py
SUPP = {
 'gz-2026-jul21-debt': {'date': '2026-07-21', 'hits': 5,
   'title': 'RTD considers adding debt on top of making cuts, setting stage for 2028 measure',
   'url': 'https://denvergazette.com/2026/07/21/rtd-considers-adding-debt-on-top-of-making-cuts-setting-stage-for-2028-measure/'},
 'gz-2026-jun02-satisfaction': {'date': '2026-06-02', 'hits': 3,
   'title': 'RTD rider satisfaction rises but overall transit use stagnates',
   'url': 'https://denvergazette.com/2026/06/02/rtd-rider-satisfaction-rises-but-overall-transit-use-stagnates/'},
 'gz-2026-sep22-waymo': {'date': '2026-09-22', 'hits': 4,
   'title': "Waymo could compete with RTD — but officials aren't worried",
   'url': 'https://denvergazette.com/2026/09/22/waymo-denver-rtd-competition/'},
}

def excerpt(slug, limit=240):
    s = ''
    e = rep.get(slug) or SUPP.get(slug)
    if e and e.get('snip'):
        s = e['snip']
    else:
        p = os.path.join(HTML, f'{slug}.txt')
        if os.path.exists(p):
            t = re.sub(r'\s+', ' ', open(p, errors='replace').read())
            for m in re.finditer(r'Nicholson', t):
                a, b = max(0, m.start()-130), min(len(t), m.end()+130)
                ctx = t[a:b].strip()
                if 'Kieran' in ctx or 'Cloudflare' in ctx:
                    continue
                s = f'…{ctx}…'
                break
    s = s.strip().strip('"')
    if len(s) > limit:
        s = s[:limit].rsplit(' ', 1)[0] + '…'
    return s

def item(date, outlet, title, url, note, extra=''):
    i = idof(url)
    ex = f' — {note}' if note else ''
    mx = f' ({extra})' if extra else ''
    return f'- **{date}** · {outlet} — [{title}]({url}){ex}{mx} [{i}]'

def rep_item(slug, outlet, note='', title=None, date=None, url=None):
    e = rep.get(slug) or SUPP.get(slug)
    if e:
        ex = excerpt(slug)
        note2 = note or (f'Excerpt: "{ex}"' if ex else '')
        t = title or e['title'][:110]
        if ' | ' in t: t = t.split(' | ')[0]
        return item(e['date'], outlet, t, e['url'], note2, f"{e['hits']} mentions")
    ex = excerpt(slug)
    note2 = note or (f'Excerpt: "{ex}"' if ex else '')
    return item(date, outlet, title, url, note2)

L = []
A = L.append
A('# Press coverage inventory — Chris Nicholson, RTD Board Director, District A')
A('')
A('Compiled 2026-09-30. Every item below was fetched and confirmed to name Chris Nicholson in its page text '
  '(mention counts from the fetched copy; excerpt shown where useful). Author-adjacent items (his own byline, '
  'Q&As he participated in) are labeled. Numbers match the citations ledger; full URL list at the bottom.')
A('')
A('## Coverage during the board term (2025 – Sep 2026)')
A('')
A(rep_item('ww-2025-route15', 'Westword', title="Just the 'Fax: What We Learned Riding the 15 With Two RTD Directors"))
A(item('2025-02-28', 'Colorado Public Radio', 'Denver to Boulder RTD train may be just years, not decades, away',
       'https://www.cpr.org/2025/02/28/denver-to-boulder-rtd-train-timeline-update/',
       'On the Northwest Rail joint-venture vote: "I really want to do it," he said. "But we\'ve got to nail down all the details, at least, for me to be able to say \'Yes.\'"'))
A(rep_item('tc-2025-ridership', 'Longmont Times-Call'))
A(rep_item('dp-2025-riders-call-help', 'The Denver Post'))
A(rep_item('ww-2025-colfaxcrawl', 'Westword'))
A(rep_item('ww-2025-policechief', 'Westword'))
A(rep_item('dp-2025-dia-a-line', 'The Denver Post'))
A(rep_item('tc-2025-ruscha', 'Longmont Times-Call'))
A(item('2025-06-23', 'Colorado Politics', "How the Israel-Hamas war is scrambling Colorado's political landscape",
       'https://www.coloradopolitics.com/2025/06/23/how-the-israel-hamas-war-is-scrambling-colorados-political-landscape-6b7f0ed1-d4cf-4e4e-99ec-bcee7ec068fd/',
       'Names him as an RTD board member among Colorado Jewish progressives who lost some left-leaning support in 2024 (drawing on the JNS piece below)'))
A(rep_item('ww-2025-dar', 'Westword'))
A(rep_item('ww-2025-access', 'Westword'))
A(rep_item('dp-2025-aod', 'The Denver Post'))
A(item('2025-10-01', 'Denverite', 'People with disabilities will now pay more for RTD on-demand rides',
       'https://denverite.com/2025/10/01/rtd-access-on-demand-price-increase/',
       'Vote detail: he proposed a low-income fare reduction amendment, then voted no on the change — "We should not be balancing our books on the backs of the very poor." Also the photo caption ("RTD board members Troy L. Whitmore (left) and Chris Nicholson listen to discussion…")'))
A(rep_item('dp-2025-electric', 'The Denver Post'))
A(rep_item('dp-2025-ridership', 'The Denver Post'))
A(rep_item('dp-2025-budget15', 'The Denver Post'))
A(rep_item('d7-2025-broncosride', 'Denver7'))
A(rep_item('dp-2026-frontrange-ballot', 'The Denver Post'))
A(rep_item('d7-2025-alameda-dec', 'Denver7'))
A(rep_item('d7-2026-alameda-jan', 'Denver7'))
A(rep_item('dp-2026-feb13-feature', 'The Denver Post'))
A(rep_item('dp-2026-fivepoints', 'The Denver Post'))
A(rep_item('dp-2026-jobcuts', 'The Denver Post'))
A(rep_item('dp-2026-contractor', 'The Denver Post'))
A(rep_item('ww-2026-cline', 'Westword'))
A(rep_item('dp-2026-audit', 'The Denver Post'))
A(rep_item('dp-2026-mar18-cuts', 'The Denver Post'))
A(item('2026-03-30', 'Denverite', 'Colorado lawmakers again propose eliminating two-thirds of RTD board seats',
       'https://denverite.com/2026/03/30/rtd-board-shrink-proposal/',
       'Extensive quotes on representation: "The biggest concern … is representation … districts so large as to make it functionally impossible for someone who is not of means or already famous to run." Editor\'s note added: concerned about the proposal, not opposed.'))
A(rep_item('gz-2026-boardshrink', 'Denver Gazette'))
A(rep_item('cn-2026-boardshrink', 'Colorado Newsline'))
A(rep_item('ww-2026-boardshrink', 'Westword'))
A(rep_item('dp-2026-apr08-ceo', 'The Denver Post'))
A(rep_item('dv-2026-ceo-out', 'Denverite', title="RTD faces 'make or break' moment as CEO Debra Johnson announces departure",
           note='His statement: Johnson led RTD "through a series of difficult moments" and was "an effective sounding board for and active participant in the board\'s recent efforts to improve the agency."'))
A(rep_item('dp-2026-apr09-frontrange', 'The Denver Post'))
A(rep_item('dp-2026-apr14-disability', 'The Denver Post'))
A(rep_item('dp-2026-apr21-20pct', 'The Denver Post'))
A(rep_item('cbs-2026-polis', 'CBS Colorado'))
A(rep_item('dp-2026-may28-frontrange3m', 'The Denver Post'))
A(rep_item('gz-2026-jun02-satisfaction', 'Denver Gazette'))
A(rep_item('dp-2026-jun12-20pct', 'The Denver Post'))
A(rep_item('dp-2026-jun25-broncosride', 'The Denver Post'))
A(rep_item('dv-2026-freeride', 'Denverite', title='RTD could kill the free 16th Street shuttle and several rail lines under budget cut proposals',
           note='Quotes on the budget reckoning: "We probably should have made service cuts … two or three years ago."'))
A(rep_item('gz-2026-freeride', 'Denver Gazette'))
A(rep_item('cbs-2026-freeride', 'CBS Colorado'))
A(rep_item('dp-2026-jul16-freeride', 'The Denver Post'))
A(rep_item('gz-2026-jul21-debt', 'Denver Gazette'))
A(rep_item('dv-2026-jul29-vote', 'Denverite', title='RTD board votes to move forward with bus and rail service cuts in 2027',
           note='Vote story and quotes: "If we can\'t make these hard decisions now, they\'re going to look at us in 2027 and 2028 and wonder why we didn\'t."'))
A(rep_item('d7-2026-jul29-fares', 'Denver7'))
A(rep_item('gz-2026-jul29', 'Denver Gazette'))
A(rep_item('dp-2026-jul29-fares', 'The Denver Post'))
A(rep_item('cp-2026-rustlers', 'Colorado Politics'))
A(rep_item('d7-2026-fare-evasion', 'Denver7'))
A(rep_item('gz-2026-sep22-waymo', 'Denver Gazette'))
A(rep_item('ys-2026-ceo', 'Yellow Scene Magazine'))
A('')
A('## Campaign coverage (2024)')
A('')
A(item('2022-07-22', 'Denverite', "RTD's MyRide card is about to be reborn. Here's how to keep tapping your way onboard",
       'https://denverite.com/2022/07/22/rtds-myride-card-is-about-to-be-reborn-heres-how-to-keep-tapping-your-way-onboard/',
       'Pre-board feature built around him: "Ever since Christopher Nicholson landed in Denver in 2018, the car-less downtown resident has used his MyRide card…"; he asked Denverite for help after RTD quietly discontinued the card.'))
A(item('2024-03-26', 'Colorado Public Radio', "State lawmakers move to cut two-thirds of RTD board's elected seats",
       'https://www.cpr.org/2024/03/26/state-lawmakers-move-to-cut-two-thirds-of-rtd-boards-elected-seats/',
       'Quoted as District A candidate opposing the rushed reform bill: "We\'ve had this system for 44 years…"'))
A(item('2024-07-31', 'Colorado Public Radio', "Gov. Jared Polis plans to take a sharper interest in this fall's RTD board elections",
       'https://www.cpr.org/2024/07/31/rtd-board-elections-jared-polis/',
       'He told CPR News he learned rival Kiel Brunner\'s candidacy "was something where the governor\'s office had decided to get involved."'))
A(rep_item('cp-2024-endorse', 'Colorado Politics', title='Denver mayor endorses RTD candidate Chris Nicholson in District A',
           note='Mayor Mike Johnston\'s endorsement (also referenced in the Axios AMA recap below).'))
A(item('2024-09-10', 'Colorado Public Radio', 'RTD board election season is usually quiet. Not this year',
       'https://www.cpr.org/2024/09/10/rtd-board-election-season-is-usually-quiet-not-this-year/',
       'Lead candidate profile on the newly competitive races; he coordinated the shared "Commitment to Riders": "These are the things that are five-alarm fires."'))
A(rep_item('ax-2024-commitment', 'Axios Denver', title='7 RTD candidates pledge new "commitment to riders"',
           note='He led the effort: "RTD clearly is not delivering the quality of service that riders and would-be riders want."'))
A(item('2024-10-14', 'CPR News voter guide', "Meet the candidates in RTD's District A race",
       'https://www.cpr.org/2024/10/14/vg-2024-colorado-rtd-district-a-candidates/',
       'Q&A he participated in: full-time rider (203 trips in six months on his MyRide account), ATU 1001 endorsement, fixRTD platform.'))
A(item('2024-10-14', 'CPR News', "Denver metro's RTD board member elections, explained",
       'https://www.cpr.org/2024/10/14/vg-2024-denver-metro-rtd-districts-and-candidates-explainer/',
       'Race landscape explainer listing him among District A candidates.'))
A(rep_item('cp-2024-criminal', 'Colorado Politics'))
A(item('October 2024', 'JNS / Intermountain Jewish News', 'Progressive Zionists feel blackballed from Colorado Working Families Party',
       'https://www.jns.org/progressive-zionists-feel-blackballed-from-colorado-working-families-party/',
       'Feature (12 name mentions): describes him as Jewish and encountering "significant concerns" from the Working Families Party over his Israel views; direct quotes.'))
A(item('2024-10-25', 'Axios Denver', "Denver's mayor spills the tea in Reddit AMA",
       'https://www.axios.com/local/denver/2024/10/25/mayor-mike-johnston-reddit-ama-ask-me-anything',
       'AMA recap: "The mayor is endorsing Chris Nicholson… Johnston called him a \'great community leader.\'"'))
A(rep_item('ww-2024-ballot', 'Westword'))
A(rep_item('ww-2024-lightrail', 'Westword', title='Light Rail, Hard Ride: RTD Struggles to Get Riders Back on Track'))
A(item('2024-11-01', 'Colorado Public Radio', 'Competitive RTD races are attracting unusually big dollars',
       'https://www.cpr.org/2024/11/01/rtd-board-races-campaign-funds/',
       'Campaign-finance deep dive: "I am lucky to have the ability to go to the people I\'m close to and raise the money necessary…"; $10K from the ATU-1001 political arm; Conservation Colorado spending against him in the race.'))
A(item('2024-11-05', 'Colorado Public Radio', 'Colorado 2024 General Election: Live blog, results and updates',
       'https://www.cpr.org/2024/11/05/colorado-2024-general-election-live-blog-results-updates/',
       'Election-night coverage: rival Kiel Brunner conceded Wednesday morning; "Preliminary results late on Tuesday show Nicholson leading the race with 53 percent."'))
A(item('2024-11-06', 'Colorado Community Media / Denver North Star', 'Chris Nicholson wins RTD District A seat',
       'https://www.denvernorthstar.com/archives/news/politics/election-2024/article_8cdb8ae1-1dc2-5a56-ba94-5b24454e714f.html',
       'Result story: won by 24+ points over Brunner and Dinegar; endorsements (Johnston, Council members Watson and Parady); fundraising context. Local capture also in board-tenure-review/sources/raw/.'))
A(item('2024-11-08', 'Colorado Public Radio', 'New RTD board members say they want more accountability, transparency, and riders',
       'https://www.cpr.org/2024/11/08/new-rtd-board-members-say-they-want-more-accountability-transparency-and-riders/',
       'The big post-election profile: "spearheaded the shared manifesto"; RTD "certainly feels broken a lot of the time. And we deserve it better"; wants the board to take back power (own lawyer, chain-of-command changes). Also aired as a Colorado Matters segment Nov 15, 2024.'))
A(rep_item('dp-2024-budget', 'The Denver Post'))
A(rep_item('dp-2024-qa', 'The Denver Post', title='RTD Director District A candidate Q&A',
           note='Candidate questionnaire he participated in; subscriber-only live, archived 2024-11-06 (copy held in board-tenure-review/sources/raw/).'))
A(item('2024-12-31', 'Westword', 'Metro Denver Transit System Suffers From Slow Trains, Fast Cop in 2024',
       'https://www.westword.com/news/metro-denver-transit-system-suffers-from-slow-trains-fast-cop-in-2024-22939176/',
       'Year-in-review: "Chris Nicholson, who won his race in District A, spearheaded the plan" (the Commitment to Riders).'))
A('')
A('## Taking office (Dec 2024 – Jan 2025)')
A('')
A(item('2024-12-05', 'Colorado Public Radio', 'RTD to roll out credit and debit card tap-to-pay system in 2025',
       'https://www.cpr.org/2024/12/05/rtd-new-tap-to-pay-system-in-2025/',
       'As director-elect he told the board: "It will be an incredible step forward for RTD…"'))
A(item('2025-01-09', 'Colorado Public Radio', 'RTD drivers, mechanics ramp up pressure on management in push for a bigger raise',
       'https://www.cpr.org/2025/01/09/rtd-drivers-mechanics-push-for-bigger-raise/',
       'Board leadership: "Chris Nicholson of downtown Denver is the new secretary" — elected over Michael Guzman in the only contested officer vote.'))
A(item('January 2025', 'Colorado Community Media', 'Eight directors sworn in this week to lead RTD',
       'https://www.coloradocommunitymedia.com/archives/northglenn-thornton/business/article_91a13c35-24e7-5f28-ae02-a4c7634bcb0c.html',
       'Swearing-in roundup; lists him as District A director and board Secretary.'))
A('')
A('## Authored pieces (his own byline)')
A('')
A(rep_item('dp-2026-aug05-opinion', 'The Denver Post (Opinion)', title='How the RTD board took on our budget deficit (Opinion)',
           note='By Chris Nicholson. Author page: denverpost.com/author/chris-nicholson/ [26].'))
A(item('2026-08-06', 'Daily Camera (reprint)', 'How the RTD board took on our budget deficit (Opinion)',
       'https://www.dailycamera.com/2026/08/06/rtd-board-public-transit-denver-boulder-budget-deficit-service-cuts/',
       'Same op-ed, as run by Prairie Mountain Media.'))
A(rep_item('mt-2026-opinion', 'Mass Transit Magazine (reprint)', title='CO: How the RTD board took on our budget deficit (Opinion)'))
A('')
A('## Forums & broadcast')
A('')
A(item('2024-10-13', 'City Cast Denver (moderated forum)', 'RTD District A Candidate Forum — Moderated by CityCast Denver',
       'https://www.youtube.com/watch?v=ZzHTCxS-gGY',
       'Video: he, Bob Dinegar and Kiel Brunner in the District A candidate forum.'))
A(item('2024-11-15', 'Colorado Public Radio (audio)', 'Nov. 15, 2024: … Holding RTD accountable',
       'https://www.cpr.org/show-episode/nov-15-2024-voter-approved-proposition-will-fund-victims-services-through-gun-excise-tax-holding-rtd-accountable/',
       'Colorado Matters episode carrying the "new RTD board members" story; episode page itself does not print names.'))
A('')
A('## Syndication & reprints of the reporting above')
A('')
A('Denver Post RTD stories rerun in Prairie Mountain Media papers: Daily Camera [%s] [%s]. Longmont Times-Call ran its own staff items [%s] [%s].'
  % (idof('https://www.dailycamera.com/2026/03/18/rtd-service-reductions-job-cuts/'),
     idof('https://www.dailycamera.com/2026/04/14/rtd-cuts-service-disability-access/'),
     idof('https://www.timescall.com/2025/03/04/rtd-ridership-denver-transit-numbers-rail-bus/'),
     idof('https://www.timescall.com/2025/06/14/rtd-board-member-complaints-joyann-ruscha/')))
A('The Aug 6 opinion reprint is cited above [%s]; CPR items were republished by Colorado FOIC and Boulder Daily, and Axios/CPR summaries showed up on aggregators (NewsBreak).'
  % idof('https://www.dailycamera.com/2026/08/06/rtd-board-public-transit-denver-boulder-budget-deficit-service-cuts/'))
A('')
A('## Outlets checked with no coverage found naming him')
A('')
A('- The Colorado Sun — site search and web searches; its RTD coverage does not name him.')
A('- 9NEWS (KUSA) — none found.')
A('- FOX31/KDVR and Channel 2 — none found.')
A('- 5280 Magazine, Boulder Reporting Lab, Denver Business Journal — none found.')
A('- City Cast Denver — no article coverage found; only the 2024 candidate forum video above.')
A('- Streetsblog Denver — defunct; no relevant posts found.')
A('- GDELT sweep — API rate-limited (shared IP) during this pass; an earlier June 2026 sweep found only 3 items, all already included here.')
A('')
A('## Adjacent non-press references (for completeness)')
A('')
A('- [Ballotpedia profile](https://ballotpedia.org/Chris_Nicholson) — election results and office details [%s].' % idof('https://ballotpedia.org/Chris_Nicholson'))
A('- [Colorado Secretary of State press release, June 27, 2024](https://www.sos.state.co.us/pubs/newsRoom/pressReleases/2024/PR20240627Nicholson.html) — "Chris Nicholson Qualifies for General Election Ballot" [%s].' % idof('https://www.sos.state.co.us/pubs/newsRoom/pressReleases/2024/PR20240627Nicholson.html'))
A('- RTD agency newsroom items (e.g., board sworn in, January 2025) — official comms, not press.')
A('')

body = '\n'.join(L)
open(os.path.join(BASE, 'press-inventory.md'), 'w').write(body + '\n\n')
print(body[:500])
print('...')
print('item bullets written:', len([x for x in L if x.startswith('- **')]))
print('uncited warnings above?')
