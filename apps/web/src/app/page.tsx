import Link from "next/link";
import { 
  ShieldCheck, Lock, Tag, Users, 
  BookOpen, Laptop, Shirt, Armchair, Dribbble, LayoutGrid, ArrowRight
} from "lucide-react";

export default function HomePage() {
  return (
    <div className="relative overflow-hidden bg-[#F8FAFC]">
      
      {/* Hero Section */}
      <section className="relative px-6 py-20 sm:py-32 flex items-center justify-center min-h-[600px]">
        {/* Background Overlay */}
        <div className="absolute inset-0 z-0">
          <div className="absolute inset-0 bg-white/70 backdrop-blur-[2px] z-10" />
          <div className="absolute inset-0 bg-gradient-to-b from-campusloop-secondary/10 to-transparent z-10" />
          {/* Note: Placeholder gradient representing the "faded/translucent" happy students image */}
          <div className="absolute inset-0 bg-slate-200 object-cover w-full h-full" />
        </div>

        <div className="relative z-20 mx-auto max-w-4xl text-center">
          <h1 className="text-5xl font-black tracking-tight text-slate-900 sm:text-7xl font-display">
            One Campus.<br />
            <span className="text-campusloop-primary">Endless Opportunities.</span>
          </h1>
          <p className="mt-6 max-w-2xl mx-auto text-lg leading-8 text-slate-600">
            The trusted marketplace exclusively for verified Strathmore University students.
          </p>
          <div className="mt-10 flex flex-col justify-center gap-4 sm:flex-row sm:items-center">
            <Link href="/auth/signup" className="inline-flex items-center justify-center rounded-full bg-campusloop-primary px-8 py-4 text-base font-semibold text-white shadow-sm transition hover:bg-campusloop-secondary gap-2">
              Get Started <ArrowRight size={18} />
            </Link>
            <Link href="/browse" className="inline-flex items-center justify-center rounded-full border border-slate-300 bg-white px-8 py-4 text-base font-semibold text-slate-800 transition hover:bg-slate-50 gap-2 shadow-sm">
              Browse Marketplace <Tag size={18} />
            </Link>
          </div>
        </div>
      </section>

      {/* Trust Highlights */}
      <section className="mx-auto max-w-6xl px-6 py-12 -mt-16 relative z-30">
        <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-4">
          <div className="rounded-2xl border border-slate-200 bg-white p-6 shadow-sm flex items-start gap-4">
            <div className="rounded-full bg-campusloop-secondary/10 p-3 text-campusloop-primary">
              <ShieldCheck size={24} />
            </div>
            <div>
              <h3 className="font-bold text-slate-900 text-sm">Verified Students</h3>
              <p className="mt-1 text-xs text-slate-500 leading-tight">Only Strathmore students can buy and sell.</p>
            </div>
          </div>
          <div className="rounded-2xl border border-slate-200 bg-white p-6 shadow-sm flex items-start gap-4">
            <div className="rounded-full bg-campusloop-secondary/10 p-3 text-campusloop-primary">
              <Lock size={24} />
            </div>
            <div>
              <h3 className="font-bold text-slate-900 text-sm">Trusted & Safe</h3>
              <p className="mt-1 text-xs text-slate-500 leading-tight">Secure transactions in a trusted environment.</p>
            </div>
          </div>
          <div className="rounded-2xl border border-slate-200 bg-white p-6 shadow-sm flex items-start gap-4">
            <div className="rounded-full bg-campusloop-secondary/10 p-3 text-campusloop-primary">
              <Tag size={24} />
            </div>
            <div>
              <h3 className="font-bold text-slate-900 text-sm">Great Deals</h3>
              <p className="mt-1 text-xs text-slate-500 leading-tight">Find quality items at student-friendly prices.</p>
            </div>
          </div>
          <div className="rounded-2xl border border-slate-200 bg-white p-6 shadow-sm flex items-start gap-4">
            <div className="rounded-full bg-campusloop-secondary/10 p-3 text-campusloop-primary">
              <Users size={24} />
            </div>
            <div>
              <h3 className="font-bold text-slate-900 text-sm">Connect & Grow</h3>
              <p className="mt-1 text-xs text-slate-500 leading-tight">Build connections beyond the classroom.</p>
            </div>
          </div>
        </div>
      </section>

      {/* Popular Categories */}
      <section className="mx-auto max-w-6xl px-6 py-20">
        <div className="flex items-center justify-between mb-8">
          <h2 className="text-2xl font-bold font-display text-slate-900">Popular Categories</h2>
          <Link href="/categories" className="text-sm font-semibold text-campusloop-primary hover:text-campusloop-secondary flex items-center gap-1">
            View all categories <ArrowRight size={16} />
          </Link>
        </div>
        <div className="grid gap-6 grid-cols-2 md:grid-cols-3 lg:grid-cols-6">
          {[
            { name: "Textbooks", icon: BookOpen, count: "120+" },
            { name: "Electronics", icon: Laptop, count: "85+" },
            { name: "Fashion", icon: Shirt, count: "95+" },
            { name: "Furniture", icon: Armchair, count: "70+" },
            { name: "Sports", icon: Dribbble, count: "60+" },
            { name: "Others", icon: LayoutGrid, count: "100+" },
          ].map((cat) => (
            <Link key={cat.name} href={`/categories/${cat.name.toLowerCase()}`} className="group rounded-2xl border border-slate-200 bg-white p-6 shadow-sm transition hover:shadow-md hover:-translate-y-1 flex flex-col items-center text-center">
              <div className="rounded-xl bg-slate-50 p-4 mb-4 text-campusloop-primary group-hover:bg-campusloop-primary/10 transition">
                <cat.icon size={32} strokeWidth={1.5} />
              </div>
              <h3 className="font-semibold text-slate-900">{cat.name}</h3>
              <p className="text-xs text-slate-500 mt-1">{cat.count} listings</p>
            </Link>
          ))}
        </div>
      </section>

      {/* How It Works */}
      <section id="how-it-works" className="bg-white border-y border-slate-200/60 py-24">
        <div className="mx-auto max-w-6xl px-6 text-center">
          <h2 className="text-3xl font-bold font-display text-slate-900 mb-16">How It Works</h2>
          <div className="grid gap-12 md:grid-cols-3">
            <div className="flex flex-col items-center">
              <div className="flex h-16 w-16 items-center justify-center rounded-full bg-campusloop-primary text-white text-xl font-bold mb-6 shadow-sm">1</div>
              <h3 className="text-xl font-semibold text-slate-900">Verify your student email</h3>
              <p className="mt-4 text-slate-600">Sign up using your Strathmore university email to access the exclusive community.</p>
            </div>
            <div className="flex flex-col items-center">
              <div className="flex h-16 w-16 items-center justify-center rounded-full bg-campusloop-primary text-white text-xl font-bold mb-6 shadow-sm">2</div>
              <h3 className="text-xl font-semibold text-slate-900">Browse or list an item</h3>
              <p className="mt-4 text-slate-600">Find great deals from fellow students or post items you want to sell in minutes.</p>
            </div>
            <div className="flex flex-col items-center">
              <div className="flex h-16 w-16 items-center justify-center rounded-full bg-campusloop-primary text-white text-xl font-bold mb-6 shadow-sm">3</div>
              <h3 className="text-xl font-semibold text-slate-900">Connect and close the deal</h3>
              <p className="mt-4 text-slate-600">Message securely on CampusLoop and arrange to meet on campus to complete the transaction.</p>
            </div>
          </div>
        </div>
      </section>

      {/* Trust Banner */}
      <section className="mx-auto max-w-6xl px-6 py-24">
        <div className="rounded-3xl bg-campusloop-primary/5 border border-campusloop-primary/20 p-12 text-center md:flex md:items-center md:justify-between md:text-left">
          <div className="flex items-center justify-center md:justify-start gap-4 mb-6 md:mb-0">
            <div className="rounded-full bg-campusloop-primary p-4 text-white">
              <ShieldCheck size={32} />
            </div>
            <div>
              <h2 className="text-2xl font-bold font-display text-slate-900">Built for Strathmore. Powered by Trust.</h2>
              <p className="mt-2 text-slate-600">Together, we create a better campus.</p>
            </div>
          </div>
          <div className="flex items-center justify-center opacity-70">
             {/* Strathmore Crest Placeholder */}
             <div className="font-bold text-xl tracking-widest text-slate-500 uppercase border-l-2 border-slate-300 pl-6 ml-2 py-2">Strathmore</div>
          </div>
        </div>
      </section>

    </div>
  );
}
