wallets = re.findall(r'(?:[13][a-km-zA-HJ-NP-Z1-9]{25,34}|0x[a-fA-F0-9]{40})', html)
            
            self.drops.extend([EntityNormalizer.normalize_drop(f"{vendor['name']} - {d}") for d in drops])
            self.wallets.extend([EntityNormalizer.normalize_wallet(w, 'BTC' if w.startswith(('1','3')) else 'ETH') for w in wallets])
    
    async def neo4j_write(self):
        """❌ Neo4j write operations"""
        with self.neo4j_driver.session() as session:
            # Clear old data
            await session.run("MATCH (n:Vendor {target: $target}) DETACH DELETE n", target=self.target)
            
            # Write vendors
            for vendor in self.vendors:
                await session.run("""
                    MERGE (v:Vendor {name: $name, target: $target})
                    SET v.rating = $rating, v.market = $market, v.listings = $listings
                    """, name=vendor['name'], target=self.target, **vendor)
    
    def export_iocs(self):
        """❌ IOCs output (CSV/JSON/STIX)"""
        iocs = {
            'vendors': self.vendors,
            'drops': self.drops,
            'wallets': self.wallets,
            'target': self.target
        }
        
        # CSV
        pd.DataFrame(iocs['vendors']).to_csv(f"iocs/{self.target}_vendors.csv", index=False)
        
        # JSON
        with open(f"iocs/{self.target}_iocs.json", 'w') as f:
            json.dump(iocs, f, indent=2)
        
        # STIX2 Bundle
        bundle_objects = [
            Indicator(name=f"Vendor {v['name']}", pattern=f"[vendor:name = '{v['name']}']", 
                     pattern_type="stix", created=datetime.now().isoformat())
            for v in iocs['vendors'][:10]
        ]
        bundle = Bundle(objects=bundle_objects)
        with open(f"iocs/{self.target}_stix.json", 'w') as f:
            f.write(bundle.serialize(pretty=True))
        
        print(f"{Fore.GREEN}✅ IOCs exported: CSV/JSON/STIX")

def main():
    target = input(f"{Fore.RED}💎 ELITE ONION COLLECTOR v5.0 > Target: ").strip()
    
    os.makedirs("iocs", exist_ok=True)
    collector = EliteOnionCollector(target)
    
    print(f"{Fore.CYAN}🚀 Collecting from {len(REAL_ONION_MARKETS)} REAL .onion markets...")
    asyncio.run(collector.collect_all())
    
    # Post-processing
    clusterer = DropClusterer()
    clusters = clusterer.cluster_drops(collector.drops)
    
    print(f"{Fore.GREEN}📊 RESULTS:")
    print(f"   Vendors: {len(collector.vendors)}")
    print(f"   Drop Clusters: {len(clusters)}")
    print(f"   Wallets: {len(collector.wallets)}")
    print(f"   Neo4j: {collector.target}")
    
    collector.export_iocs()
    print(f"{Fore.RED}💎 ELITE COLLECTION COMPLETE")

if name == "main":
    print("""
💎 ELITE ONION COLLECTOR v5.0 - PRODUCTION
┌─────────────────────────────────────────────────────┐
│  Real .onion • Vendors • Drops • Multi-chain        │
│  Neo4j • STIX • Geospatial • OpSec TTPs             │
│              DARK MARKET INTEL SUITE                 │
└─────────────────────────────────────────────────────┘
    """)
    main()
