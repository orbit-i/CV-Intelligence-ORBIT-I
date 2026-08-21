import { useState, useMemo } from "react";
import {
  Search, Plus, ChevronDown, Bell, User, LayoutDashboard,
  Briefcase, Users, UserCheck, CalendarDays, BarChart2,
  Settings, Filter, Calendar, ChevronLeft, ChevronRight,
  AlignJustify,
} from "lucide-react";

/* ─────────────────────────────────────────────────────────────
   ORBIT-I  ·  Organization Admin Portal
   Candidates + Recruiters + Interviews
───────────────────────────────────────────────────────────── */

const C = {
  sidebarBg:         "#1B2A6B",
  sidebarActive:     "#2D3E99",
  sidebarText:       "#A8B8E8",
  sidebarActiveText: "#FFFFFF",
  sidebarIcon:       "#7A8EC8",
  bg:                "#F0F3FB",
  surface:           "#FFFFFF",
  border:            "#E2E8F2",
  ink:               "#1A1D2E",
  muted:             "#7A8099",
  accent:            "#4F6FE8",
  green:             "#22B07D",
  orange:            "#F59E0B",
  red:               "#EF4444",
  purple:            "#8B5CF6",
};

const STAGE_COLORS = {
  "In Interview": { text: "#F59E0B", bg: "#FEF9EC" },
  Screening:      { text: "#4F6FE8", bg: "#EEF2FF" },
  Assessment:     { text: "#8B5CF6", bg: "#F5F3FF" },
  Asessment:      { text: "#8B5CF6", bg: "#F5F3FF" },
  Shortlisted:    { text: "#22B07D", bg: "#ECFDF5" },
  Applied:        { text: "#4F6FE8", bg: "#EEF2FF" },
  Rejected:       { text: "#EF4444", bg: "#FEF2F2" },
  Hired:          { text: "#22B07D", bg: "#ECFDF5" },
};

const RECRUITER_STATUS = {
  Active:   { text: "#22B07D", bg: "#ECFDF5" },
  Away:     { text: "#F59E0B", bg: "#FEF9EC" },
  InActive: { text: "#EF4444", bg: "#FEF2F2" },
};

const INTERVIEW_STATUS = {
  Scheduled: { text: "#4F6FE8", bg: "#EEF2FF" },
  Completed: { text: "#22B07D", bg: "#ECFDF5" },
  Cancelled: { text: "#EF4444", bg: "#FEF2F2" },
};

/* ── Data ── */
const CANDIDATES = [
  { id:1,  name:"sarah khan",  jobTitle:"UI/UX Designer",    dept:"Designer",    loc:"Remote",         applicants:42, stage:"In Interview", date:"Jul,20, 2026"   },
  { id:2,  name:"John Smith",  jobTitle:"Frontend Developer", dept:"Engineer",   loc:"Lahore, pak",    applicants:35, stage:"Screening",    date:"Jul,16, 20206"  },
  { id:3,  name:"maryam",      jobTitle:"Backend Engineer",   dept:"Engineer",   loc:"Karachi, pak",   applicants:18, stage:"Asessment",    date:"jul,15, 2026"   },
  { id:4,  name:"Ayesha Khan", jobTitle:"HR Executive",       dept:"H Resources",loc:"Islamabad, pak", applicants:26, stage:"Shortlisted",  date:"Jul,14 2026"    },
  { id:5,  name:"Muneeb",      jobTitle:"Data Analyst",       dept:"Analyst",    loc:"Lahore,pak",     applicants:14, stage:"Applied",      date:"Jul,13 2026"    },
  { id:6,  name:"olivia",      jobTitle:"Market Specialist",  dept:"Market",     loc:"Remote",         applicants:31, stage:"Rejected",     date:"Jul, 12, 2026"  },
];

const RECRUITERS = [
  { id:1, name:"sarah khan",  jobTitle:"UI/UX Designer",    dept:"Designer",    loc:"Remote",         assignedJobs:12, status:"Active",   date:"Jul,20, 2026"  },
  { id:2, name:"John Smith",  jobTitle:"Frontend Developer", dept:"Engineer",   loc:"Lahore, pak",    assignedJobs:5,  status:"Active",   date:"Jul,16, 20206" },
  { id:3, name:"maryam",      jobTitle:"Backend Engineer",   dept:"Engineer",   loc:"Karachi, pak",   assignedJobs:16, status:"Active",   date:"jul,15, 2026"  },
  { id:4, name:"Ayesha Khan", jobTitle:"HR Executive",       dept:"H Resources",loc:"Islamabad, pak", assignedJobs:9,  status:"Away",     date:"Jul,14 2026"   },
  { id:5, name:"Muneeb",      jobTitle:"Data Analyst",       dept:"Analyst",    loc:"Lahore,pak",     assignedJobs:7,  status:"Active",   date:"Jul,13 2026"   },
  { id:6, name:"olivia",      jobTitle:"Market Specialist",  dept:"Market",     loc:"Remote",         assignedJobs:11, status:"InActive", date:"Jul, 12, 2026" },
];

const INTERVIEWS = [
  { id:1, candidate:"Sana Malik",     role:"Product Designer",    dept:"Design",      loc:"Remote",    type:"Final Round",     date:"21 Aug", time:"11:00 AM", status:"Scheduled" },
  { id:2, candidate:"Fahad Rehman",   role:"Sales Associate",     dept:"Sales",       loc:"Lahore",    type:"HR Round",        date:"21 Aug", time:"2:30 PM",  status:"Scheduled" },
  { id:3, candidate:"Bilal Ahmed",    role:"Backend Engineer",    dept:"Engineering", loc:"Lahore",    type:"Technical Round", date:"20 Aug", time:"4:00 PM",  status:"Completed" },
  { id:4, candidate:"Zainab Raza",    role:"Data Analyst",        dept:"Product",     loc:"Karachi",   type:"Screening Call",  date:"18 Aug", time:"10:00 AM", status:"Completed" },
  { id:5, candidate:"Omar Farooq",    role:"Marketing Executive", dept:"Marketing",   loc:"Lahore",    type:"HR Round",        date:"17 Aug", time:"1:00 PM",  status:"Cancelled" },
  { id:6, candidate:"Mehak Siddiqui", role:"UI/UX Designer",      dept:"Design",      loc:"Remote",    type:"Technical Round", date:"22 Aug", time:"3:00 PM",  status:"Scheduled" },
  { id:7, candidate:"Talha Nadeem",   role:"DevOps Engineer",     dept:"Engineering", loc:"Islamabad", type:"Screening Call",  date:"23 Aug", time:"9:30 AM",  status:"Scheduled" },
  { id:8, candidate:"Usman Tariq",    role:"Backend Engineer",    dept:"Engineering", loc:"Karachi",   type:"Final Round",     date:"15 Aug", time:"12:00 PM", status:"Completed" },
];

const DEPARTMENTS = ["Designer","Engineer","H Resources","Analyst","Market","Engineering","Product","Marketing","Sales"];
const JOB_TITLES  = [...new Set(CANDIDATES.map(c => c.jobTitle))];
const ALL_STAGES  = ["In Interview","Screening","Asessment","Shortlisted","Applied","Rejected","Hired"];
const ALL_STATUSES_R = ["Active","Away","InActive"];

/* ── Sparkline ── */
function Spark({ color, v = 0 }) {
  const paths = [
    "M0,14 C6,10 10,18 16,10 C22,2 28,16 34,8 C38,4 42,10 46,7",
    "M0,18 C8,14 16,10 22,8 C30,6 38,4 46,2",
    "M0,4  C8,8  16,14 22,16 C30,18 38,12 46,8",
    "M0,14 L8,6  L16,14 L24,4 L32,14 L40,8  L46,12",
  ];
  return (
    <svg width="46" height="22" viewBox="0 0 46 22" fill="none">
      <path d={paths[v % paths.length]} stroke={color} strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round" />
    </svg>
  );
}

/* ── Stat Card ── */
function StatCard({ icon: Icon, iconColor, iconBg, label, value, pct, pctUp, sparkColor, sv }) {
  return (
    <div className="rounded-2xl p-4 flex flex-col gap-2" style={{ background: C.surface, border: `1px solid ${C.border}` }}>
      <div className="flex items-center gap-2">
        <span className="w-7 h-7 rounded-lg flex items-center justify-center shrink-0" style={{ background: iconBg }}>
          <Icon className="w-3.5 h-3.5" style={{ color: iconColor }} />
        </span>
        <span className="text-[12px] font-semibold" style={{ color: iconColor }}>{label}</span>
      </div>
      <div className="flex items-end justify-between">
        <span className="text-[28px] font-bold leading-none" style={{ color: C.ink }}>{value}</span>
        <Spark color={sparkColor} v={sv} />
      </div>
      <div className="flex items-center gap-1.5">
        <span className="text-[11px] font-semibold" style={{ color: pctUp ? C.green : C.red }}>
          {pctUp ? "↑" : "↓"} {pct}
        </span>
        <span className="text-[11px]" style={{ color: C.muted }}>Vs 30 last days</span>
      </div>
    </div>
  );
}

/* ── Pagination ── */
function Pagination({ label, page, onPage }) {
  return (
    <div className="flex items-center justify-between px-4 py-3" style={{ borderTop: `1px solid ${C.border}` }}>
      <span className="text-[12px]" style={{ color: C.muted }}>{label}</span>
      <div className="flex items-center gap-1">
        {[ChevronLeft, null, null, null, null, null, ChevronRight].map((Icon, i) => {
          if (Icon) {
            return (
              <button key={i} onClick={() => onPage(i === 0 ? Math.max(1, page - 1) : page + 1)}
                className="w-7 h-7 rounded-md flex items-center justify-center"
                style={{ border: `1px solid ${C.border}`, color: C.muted, background: C.surface }}>
                <Icon className="w-3.5 h-3.5" />
              </button>
            );
          }
          const p = i; // pages 1–5
          return (
            <button key={i} onClick={() => onPage(p)}
              className="w-7 h-7 rounded-md flex items-center justify-center text-[12px] font-medium"
              style={{
                background: page === p ? C.accent : C.surface,
                color:      page === p ? "#fff"   : C.muted,
                border:     page === p ? "none"   : `1px solid ${C.border}`,
              }}>
              {p}
            </button>
          );
        })}
      </div>
    </div>
  );
}

/* ── tiny helpers ── */
function initials(n) { return n.split(" ").map(w => w[0]).slice(0, 2).join("").toUpperCase(); }
function Avatar({ name }) {
  return (
    <div className="w-8 h-8 rounded-full flex items-center justify-center text-[10px] font-bold shrink-0"
      style={{ background: "#EEF2FF", color: C.accent }}>
      {initials(name)}
    </div>
  );
}
function Badge({ label, map }) {
  const c = map[label] || { text: C.muted, bg: "#F3F4F6" };
  return (
    <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-[11px] font-semibold whitespace-nowrap"
      style={{ background: c.bg, color: c.text }}>
      {label}
    </span>
  );
}
function Th({ children }) {
  return (
    <th className="text-left text-[12px] font-semibold px-4 py-3 whitespace-nowrap"
      style={{ color: C.ink, borderBottom: `1px solid ${C.border}`, background: C.surface }}>
      {children}
    </th>
  );
}
function Td({ children, muted }) {
  return (
    <td className="px-4 py-[11px] text-[13px] align-middle whitespace-nowrap"
      style={{ color: muted ? C.muted : C.ink, borderBottom: `1px solid ${C.border}` }}>
      {children}
    </td>
  );
}
function DropSelect({ value, onChange, options, placeholder }) {
  return (
    <div className="relative">
      <select value={value} onChange={e => onChange(e.target.value)}
        className="appearance-none h-9 pl-3 pr-7 rounded-lg text-[12px] font-medium outline-none cursor-pointer"
        style={{ background: C.surface, border: `1px solid ${C.border}`, color: value ? C.ink : C.muted }}>
        <option value="">{placeholder}</option>
        {options.map(o => <option key={o} value={o}>{o}</option>)}
      </select>
      <ChevronDown className="w-3 h-3 absolute right-2 top-1/2 -translate-y-1/2 pointer-events-none" style={{ color: C.muted }} />
    </div>
  );
}

/* ─────────────────────────────────────────────────────────────
   CANDIDATES SCREEN
───────────────────────────────────────────────────────────── */
function CandidatesScreen() {
  const [q, setQ]           = useState("");
  const [job, setJob]       = useState("");
  const [status, setStatus] = useState("");
  const [page, setPage]     = useState(1);

  const rows = useMemo(() =>
    CANDIDATES.filter(c =>
      (c.name.toLowerCase().includes(q.toLowerCase()) || c.jobTitle.toLowerCase().includes(q.toLowerCase())) &&
      (!job    || c.jobTitle === job) &&
      (!status || c.stage    === status)
    ), [q, job, status]);

  return (
    <div>
      {/* Header */}
      <div className="flex items-start justify-between flex-wrap gap-3 mb-5">
        <div>
          <h1 className="text-[22px] font-bold" style={{ color: C.ink }}>Candidates</h1>
          <p className="text-[13px] mt-0.5" style={{ color: C.muted }}>Browse, search and manage all Candidates.</p>
        </div>
        <div className="flex items-center gap-2 h-9 px-3 rounded-lg text-[12px]"
          style={{ background: C.surface, border: `1px solid ${C.border}`, color: C.muted }}>
          <Calendar className="w-3.5 h-3.5" />
          Jul,13 2026 – jul, 20,2026
        </div>
      </div>

      {/* Stat cards */}
      <div className="grid grid-cols-2 lg:grid-cols-4 gap-3 mb-5">
        <StatCard icon={Users}       iconColor="#4F6FE8" iconBg="#EEF2FF" label="Total Candidates" value="1,245" pct="12.5%" pctUp sparkColor="#4F6FE8" sv={1} />
        <StatCard icon={UserCheck}   iconColor="#22B07D" iconBg="#ECFDF5" label="New Candidates"   value="256"   pct="18.5%" pctUp sparkColor="#22B07D" sv={0} />
        <StatCard icon={CalendarDays}iconColor="#8B5CF6" iconBg="#F5F3FF" label="In Interview"     value="277"   pct="8.3%"  pctUp sparkColor="#8B5CF6" sv={3} />
        <StatCard icon={Briefcase}   iconColor="#F59E0B" iconBg="#FEF9EC" label="Hired"            value="54"    pct="15.2%" pctUp sparkColor="#F59E0B" sv={2} />
      </div>

      {/* Toolbar */}
      <div className="flex flex-wrap items-center gap-2 mb-4">
        <div className="relative flex-1 min-w-[200px]">
          <Search className="w-4 h-4 absolute left-3 top-1/2 -translate-y-1/2" style={{ color: C.muted }} />
          <input value={q} onChange={e => setQ(e.target.value)} placeholder="Search names by Title, Department"
            className="w-full h-9 pl-9 pr-3 rounded-lg text-[13px] outline-none"
            style={{ background: C.surface, border: `1px solid ${C.border}`, color: C.ink }} />
        </div>
        <DropSelect value={job}    onChange={setJob}    options={JOB_TITLES}   placeholder="All Jobs"    />
        <DropSelect value={status} onChange={setStatus} options={ALL_STAGES}   placeholder="All Status"  />
        <button className="h-9 px-3.5 rounded-lg flex items-center gap-1.5 text-[12px] font-semibold"
          style={{ background: C.surface, border: `1px solid ${C.border}`, color: C.ink }}>
          <Filter className="w-3.5 h-3.5" /> Filter
        </button>
      </div>

      {/* Table */}
      <div className="rounded-2xl overflow-hidden" style={{ background: C.surface, border: `1px solid ${C.border}` }}>
        <div className="overflow-x-auto">
          <table className="w-full min-w-[820px] border-collapse">
            <thead>
              <tr>
                <Th>Names</Th><Th>Job Title</Th><Th>Department</Th>
                <Th>Location</Th><Th>Applicants</Th><Th>Stage</Th><Th>Date</Th>
              </tr>
            </thead>
            <tbody>
              {rows.map(c => (
                <tr key={c.id} className="hover:bg-slate-50 transition-colors">
                  <Td><div className="flex items-center gap-2.5"><Avatar name={c.name} /><span className="font-medium">{c.name}</span></div></Td>
                  <Td>{c.jobTitle}</Td>
                  <Td muted>{c.dept}</Td>
                  <Td muted>{c.loc}</Td>
                  <Td><span className="font-medium">{c.applicants}</span></Td>
                  <Td><Badge label={c.stage} map={STAGE_COLORS} /></Td>
                  <Td muted>{c.date}</Td>
                </tr>
              ))}
              {rows.length === 0 && (
                <tr><td colSpan={7} className="py-12 text-center text-[13px]" style={{ color: C.muted }}>No candidates match your search.</td></tr>
              )}
            </tbody>
          </table>
        </div>
        <Pagination label={`Showing 1 to 6 of 1,245 Candidates`} page={page} onPage={setPage} />
      </div>
    </div>
  );
}

/* ─────────────────────────────────────────────────────────────
   RECRUITERS SCREEN
───────────────────────────────────────────────────────────── */
function RecruitersScreen() {
  const [q, setQ]           = useState("");
  const [dept, setDept]     = useState("");
  const [status, setStatus] = useState("");
  const [page, setPage]     = useState(1);

  const rows = useMemo(() =>
    RECRUITERS.filter(r =>
      (r.name.toLowerCase().includes(q.toLowerCase()) || r.jobTitle.toLowerCase().includes(q.toLowerCase())) &&
      (!dept   || r.dept   === dept) &&
      (!status || r.status === status)
    ), [q, dept, status]);

  return (
    <div>
      {/* Header */}
      <div className="flex items-start justify-between flex-wrap gap-3 mb-5">
        <div>
          <h1 className="text-[22px] font-bold" style={{ color: C.ink }}>Recruiters</h1>
          <p className="text-[13px] mt-0.5" style={{ color: C.muted }}>Manage and monitor all recruiters in your organization.</p>
        </div>
        <button className="inline-flex items-center gap-1.5 h-9 px-4 rounded-lg text-[13px] font-semibold"
          style={{ background: C.accent, color: "#fff" }}>
          <Plus className="w-4 h-4" /> Add Recruiter
        </button>
      </div>

      {/* Stat cards */}
      <div className="grid grid-cols-2 lg:grid-cols-4 gap-3 mb-5">
        <StatCard icon={Users}       iconColor="#4F6FE8" iconBg="#EEF2FF" label="Total Recruiters"  value="28" pct="12.5%" pctUp sparkColor="#4F6FE8" sv={1} />
        <StatCard icon={UserCheck}   iconColor="#22B07D" iconBg="#ECFDF5" label="Active Recruiters" value="22" pct="18.5%" pctUp sparkColor="#22B07D" sv={0} />
        <StatCard icon={Briefcase}   iconColor="#8B5CF6" iconBg="#F5F3FF" label="Open Positions"    value="46" pct="15.2%" pctUp sparkColor="#8B5CF6" sv={3} />
        <StatCard icon={CalendarDays}iconColor="#F59E0B" iconBg="#FEF9EC" label="Assigned Jobs"     value="89" pct="8.3%"  pctUp={false} sparkColor="#F59E0B" sv={2} />
      </div>

      {/* Toolbar */}
      <div className="flex flex-wrap items-center gap-2 mb-4">
        <div className="relative flex-1 min-w-[200px]">
          <Search className="w-4 h-4 absolute left-3 top-1/2 -translate-y-1/2" style={{ color: C.muted }} />
          <input value={q} onChange={e => setQ(e.target.value)} placeholder="Search Recruiter by Title jobs, Department"
            className="w-full h-9 pl-9 pr-3 rounded-lg text-[13px] outline-none"
            style={{ background: C.surface, border: `1px solid ${C.border}`, color: C.ink }} />
        </div>
        <DropSelect value={dept}   onChange={setDept}   options={DEPARTMENTS}       placeholder="All Departments" />
        <DropSelect value={status} onChange={setStatus} options={ALL_STATUSES_R}    placeholder="All Status"      />
        <button className="h-9 px-3.5 rounded-lg flex items-center gap-1.5 text-[12px] font-semibold"
          style={{ background: C.surface, border: `1px solid ${C.border}`, color: C.ink }}>
          <Filter className="w-3.5 h-3.5" /> Filter
        </button>
      </div>

      {/* Table */}
      <div className="rounded-2xl overflow-hidden" style={{ background: C.surface, border: `1px solid ${C.border}` }}>
        <div className="overflow-x-auto">
          <table className="w-full min-w-[860px] border-collapse">
            <thead>
              <tr>
                <Th>Recruiter</Th><Th>Job Title</Th><Th>Department</Th>
                <Th>Location</Th><Th>Assigned Jobs</Th><Th>Status</Th><Th>Date</Th>
              </tr>
            </thead>
            <tbody>
              {rows.map(r => (
                <tr key={r.id} className="hover:bg-slate-50 transition-colors">
                  <Td><div className="flex items-center gap-2.5"><Avatar name={r.name} /><span className="font-medium">{r.name}</span></div></Td>
                  <Td>{r.jobTitle}</Td>
                  <Td muted>{r.dept}</Td>
                  <Td muted>{r.loc}</Td>
                  <Td><span className="font-medium">{r.assignedJobs}</span></Td>
                  <Td><Badge label={r.status} map={RECRUITER_STATUS} /></Td>
                  <Td muted>{r.date}</Td>
                </tr>
              ))}
              {rows.length === 0 && (
                <tr><td colSpan={7} className="py-12 text-center text-[13px]" style={{ color: C.muted }}>No recruiters match your search.</td></tr>
              )}
            </tbody>
          </table>
        </div>
        <Pagination label={`Showing 1 to 8 of 28 Recruiters`} page={page} onPage={setPage} />
      </div>
    </div>
  );
}

/* ─────────────────────────────────────────────────────────────
   INTERVIEWS SCREEN
───────────────────────────────────────────────────────────── */
function InterviewsScreen() {
  const [q, setQ]           = useState("");
  const [type, setType]     = useState("");
  const [status, setStatus] = useState("");
  const [page, setPage]     = useState(1);

  const TYPES = [...new Set(INTERVIEWS.map(i => i.type))];

  const rows = useMemo(() =>
    INTERVIEWS.filter(i =>
      (i.candidate.toLowerCase().includes(q.toLowerCase()) ||
       i.role.toLowerCase().includes(q.toLowerCase())) &&
      (!type   || i.type   === type) &&
      (!status || i.status === status)
    ), [q, type, status]);

  return (
    <div>
      {/* Header */}
      <div className="flex items-start justify-between flex-wrap gap-3 mb-5">
        <div>
          <h1 className="text-[22px] font-bold" style={{ color: C.ink }}>Interviews</h1>
          <p className="text-[13px] mt-0.5" style={{ color: C.muted }}>Browse, search and manage all scheduled interviews.</p>
        </div>
        <button
          className="inline-flex items-center gap-1.5 h-9 px-4 rounded-lg text-[13px] font-semibold"
          style={{ background: C.accent, color: "#fff" }}>
          <Plus className="w-4 h-4" /> Schedule Interview
        </button>
      </div>

      {/* Stat cards */}
      <div className="grid grid-cols-2 lg:grid-cols-4 gap-3 mb-5">
        <StatCard
          icon={CalendarDays} iconColor="#4F6FE8" iconBg="#EEF2FF"
          label="Total Interviews" value={String(INTERVIEWS.length)}
          pct="10.5%" pctUp sparkColor="#4F6FE8" sv={1}
        />
        <StatCard
          icon={UserCheck} iconColor="#22B07D" iconBg="#ECFDF5"
          label="Scheduled" value={String(INTERVIEWS.filter(i => i.status === "Scheduled").length)}
          pct="14.2%" pctUp sparkColor="#22B07D" sv={0}
        />
        <StatCard
          icon={Briefcase} iconColor="#8B5CF6" iconBg="#F5F3FF"
          label="Completed" value={String(INTERVIEWS.filter(i => i.status === "Completed").length)}
          pct="9.1%" pctUp sparkColor="#8B5CF6" sv={3}
        />
        <StatCard
          icon={Users} iconColor="#EF4444" iconBg="#FEF2F2"
          label="Cancelled" value={String(INTERVIEWS.filter(i => i.status === "Cancelled").length)}
          pct="3.0%" pctUp={false} sparkColor="#EF4444" sv={2}
        />
      </div>

      {/* Toolbar */}
      <div className="flex flex-wrap items-center gap-2 mb-4">
        <div className="relative flex-1 min-w-[200px]">
          <Search className="w-4 h-4 absolute left-3 top-1/2 -translate-y-1/2" style={{ color: C.muted }} />
          <input
            value={q} onChange={e => setQ(e.target.value)}
            placeholder="Search by Candidate name, Job Title"
            className="w-full h-9 pl-9 pr-3 rounded-lg text-[13px] outline-none"
            style={{ background: C.surface, border: `1px solid ${C.border}`, color: C.ink }}
          />
        </div>
        <DropSelect value={type}   onChange={setType}   options={TYPES}                              placeholder="All Types"    />
        <DropSelect value={status} onChange={setStatus} options={["Scheduled","Completed","Cancelled"]} placeholder="All Status"   />
        <button
          className="h-9 px-3.5 rounded-lg flex items-center gap-1.5 text-[12px] font-semibold"
          style={{ background: C.surface, border: `1px solid ${C.border}`, color: C.ink }}>
          <Filter className="w-3.5 h-3.5" /> Filter
        </button>
      </div>

      {/* Table */}
      <div className="rounded-2xl overflow-hidden" style={{ background: C.surface, border: `1px solid ${C.border}` }}>
        <div className="overflow-x-auto">
          <table className="w-full min-w-[860px] border-collapse">
            <thead>
              <tr>
                <Th>Candidate</Th>
                <Th>Job Title</Th>
                <Th>Department</Th>
                <Th>Location</Th>
                <Th>Interview Type</Th>
                <Th>Date & Time</Th>
                <Th>Status</Th>
              </tr>
            </thead>
            <tbody>
              {rows.map(i => (
                <tr key={i.id} className="hover:bg-slate-50 transition-colors">
                  <Td>
                    <div className="flex items-center gap-2.5">
                      <Avatar name={i.candidate} />
                      <span className="font-medium">{i.candidate}</span>
                    </div>
                  </Td>
                  <Td>{i.role}</Td>
                  <Td muted>{i.dept}</Td>
                  <Td muted>{i.loc}</Td>
                  <Td muted>{i.type}</Td>
                  <Td muted>{i.date}, {i.time}</Td>
                  <Td><Badge label={i.status} map={INTERVIEW_STATUS} /></Td>
                </tr>
              ))}
              {rows.length === 0 && (
                <tr>
                  <td colSpan={7} className="py-12 text-center text-[13px]" style={{ color: C.muted }}>
                    No interviews match your search.
                  </td>
                </tr>
              )}
            </tbody>
          </table>
        </div>
        <Pagination
          label={`Showing 1 to ${rows.length} of ${INTERVIEWS.length} Interviews`}
          page={page}
          onPage={setPage}
        />
      </div>
    </div>
  );
}

/* ─────────────────────────────────────────────────────────────
   SIDEBAR NAV
───────────────────────────────────────────────────────────── */
const NAV = [
  { id:"dashboard",  label:"Dashboard",  Icon: LayoutDashboard },
  { id:"jobs",       label:"Jobs",       Icon: Briefcase       },
  { id:"candidates", label:"Candidates", Icon: Users           },
  { id:"recruiters", label:"Recruiters", Icon: UserCheck       },
  { id:"interviews", label:"Interviews", Icon: CalendarDays    },
  { id:"report",     label:"Report",     Icon: BarChart2       },
  { id:"settings",   label:"Settings",   Icon: Settings        },
];

function Sidebar({ tab, setTab }) {
  return (
    <aside className="flex flex-col h-full" style={{ background: C.sidebarBg, width: 200 }}>
      {/* Logo */}
      <div className="flex flex-col items-center pt-6 pb-4 px-4">
        {/* Orbit logo circle */}
        <div className="w-16 h-16 rounded-full flex items-center justify-center mb-3 relative"
          style={{ background: "radial-gradient(circle at 40% 40%, #2D3E99, #0D1440)" }}>
          {/* ring */}
          <svg width="64" height="64" viewBox="0 0 64 64" className="absolute inset-0">
            <ellipse cx="32" cy="32" rx="28" ry="11" stroke="#4F6FE8" strokeWidth="1.5" fill="none"
              transform="rotate(-30 32 32)" />
            <circle cx="32" cy="32" r="8" fill="#1B2A6B" />
            <circle cx="32" cy="32" r="5" fill="#4F6FE8" opacity="0.9" />
            <circle cx="52" cy="22" r="3" fill="#4F6FE8" />
          </svg>
        </div>
        <div className="text-center">
          <div className="text-[15px] font-bold tracking-widest" style={{ color: "#fff", letterSpacing: "0.15em" }}>ORBIT-I</div>
          <div className="text-[9px] tracking-wider mt-0.5" style={{ color: C.sidebarText, letterSpacing: "0.08em" }}>BUILDING IDEAS · CREATING IMPACT</div>
        </div>
      </div>

      {/* Nav items */}
      <nav className="flex-1 px-3 mt-3 flex flex-col gap-0.5">
        {NAV.map(({ id, label, Icon }) => {
          const active = tab === id;
          return (
            <button key={id} onClick={() => setTab(id)}
              className="flex items-center gap-3 w-full px-3 py-2.5 rounded-xl text-[13px] font-medium text-left transition-colors"
              style={{
                background: active ? C.sidebarActive : "transparent",
                color:      active ? C.sidebarActiveText : C.sidebarText,
              }}>
              <Icon className="w-4 h-4 shrink-0" />
              {label}
            </button>
          );
        })}
      </nav>

      {/* User footer */}
      <div className="px-3 py-4 flex items-center gap-2.5" style={{ borderTop: `1px solid #2D3E6620` }}>
        <div className="w-8 h-8 rounded-full flex items-center justify-center shrink-0"
          style={{ background: "#2D3E99" }}>
          <User className="w-4 h-4" style={{ color: "#A8B8E8" }} />
        </div>
        <div className="min-w-0">
          <div className="text-[12px] font-semibold truncate" style={{ color: "#fff" }}>Elisa musk</div>
          <div className="text-[10px] truncate" style={{ color: C.sidebarText }}>elisamusk@gmail.com</div>
        </div>
      </div>
    </aside>
  );
}

/* ─────────────────────────────────────────────────────────────
   TOP BAR
───────────────────────────────────────────────────────────── */
function TopBar() {
  return (
    <header className="h-14 flex items-center justify-between px-6 shrink-0"
      style={{ background: C.surface, borderBottom: `1px solid ${C.border}` }}>
      <div className="flex items-center gap-2" style={{ color: C.muted }}>
        <AlignJustify className="w-4 h-4" />
        <span className="text-[14px] font-semibold" style={{ color: C.ink }}>Organization Admin Portal</span>
      </div>
      <div className="flex items-center gap-3">
        {/* search */}
        <div className="relative hidden sm:block">
          <Search className="w-3.5 h-3.5 absolute left-3 top-1/2 -translate-y-1/2" style={{ color: C.muted }} />
          <input placeholder="Search Anything"
            className="h-8 pl-8 pr-3 rounded-lg text-[12px] outline-none w-48"
            style={{ background: C.bg, border: `1px solid ${C.border}`, color: C.ink }} />
        </div>
        {/* bell */}
        <button className="w-8 h-8 rounded-full flex items-center justify-center"
          style={{ background: C.bg, border: `1px solid ${C.border}` }}>
          <Bell className="w-4 h-4" style={{ color: C.muted }} />
        </button>
        {/* avatar */}
        <button className="w-8 h-8 rounded-full flex items-center justify-center"
          style={{ background: C.bg, border: `1px solid ${C.border}` }}>
          <User className="w-4 h-4" style={{ color: C.muted }} />
        </button>
      </div>
    </header>
  );
}

/* ─────────────────────────────────────────────────────────────
   APP ROOT
───────────────────────────────────────────────────────────── */
export default function App() {
  const [tab, setTab] = useState("candidates");

  return (
    <div className="flex h-screen w-full overflow-hidden" style={{ background: C.bg, fontFamily: "'Inter', 'Segoe UI', sans-serif" }}>
      <style>{`
        * { box-sizing: border-box; }
        ::-webkit-scrollbar { width: 4px; height: 4px; }
        ::-webkit-scrollbar-track { background: transparent; }
        ::-webkit-scrollbar-thumb { background: #CBD5E1; border-radius: 4px; }
        select option { color: #1A1D2E; background: #fff; }
      `}</style>

      {/* Sidebar */}
      <Sidebar tab={tab} setTab={setTab} />

      {/* Main */}
      <div className="flex flex-col flex-1 min-w-0 overflow-hidden">
        <TopBar />
        <main className="flex-1 overflow-y-auto p-6">
          {tab === "candidates"  && <CandidatesScreen />}
          {tab === "recruiters"  && <RecruitersScreen />}
          {tab === "interviews"  && <InterviewsScreen />}
          {(tab === "dashboard" || tab === "jobs" || tab === "report" || tab === "settings") && (
            <div className="flex items-center justify-center h-full">
              <p className="text-[14px]" style={{ color: C.muted }}>
                {tab.charAt(0).toUpperCase() + tab.slice(1)} page coming soon.
              </p>
            </div>
          )}
        </main>
      </div>
    </div>
  );
}
