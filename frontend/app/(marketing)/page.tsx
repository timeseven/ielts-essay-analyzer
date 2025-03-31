import CTA from '@/components/marketing/CTA';
import Features from '@/components/marketing/Features';
import Footer from '@/components/marketing/Footer';
import Header from '@/components/marketing/Header';
import Hero from '@/components/marketing/Hero';
import Testimonials from '@/components/marketing/Testimonials';
import ScrollToTopButton from '@/components/ScrollToTopButton';
import React from 'react';

export default function MarketingPage() {
	return (
		<main className='flex min-h-screen flex-col'>
			<Header />
			<Hero />
			<div className='bg-white'>
				<Features />
				<Testimonials />
				{/* <Pricing /> */}
				<CTA />
			</div>
			<Footer />
			<ScrollToTopButton />
		</main>
	);
}
