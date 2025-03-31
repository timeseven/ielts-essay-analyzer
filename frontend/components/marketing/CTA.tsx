'use client';

import Link from 'next/link';
import { Button } from '@/components/ui/button';
import { motion } from 'motion/react';

export default function CTA() {
	return (
		<section className='w-full bg-blue-600 py-12 text-white md:py-24 lg:py-32'>
			<div className='container mx-auto px-4 text-center md:px-6'>
				<motion.h2
					className='mb-4 text-3xl font-bold'
					initial={{ opacity: 0, y: 20 }}
					animate={{ opacity: 1, y: 0 }}
					transition={{ duration: 0.5 }}
				>
					Ready to analyze your IELTS essays?
				</motion.h2>
				<motion.p
					className='mx-auto mb-8 max-w-2xl'
					initial={{ opacity: 0, y: 20 }}
					animate={{ opacity: 1, y: 0 }}
					transition={{ duration: 0.5, delay: 0.2 }}
				>
					Experience the power of AI-Powered Essay Analysis and unlock your IELTS success.
				</motion.p>
				<motion.div
					initial={{ opacity: 0, y: 20 }}
					animate={{ opacity: 1, y: 0 }}
					transition={{ duration: 0.5, delay: 0.4 }}
				>
					<Link href='/client'>
						<Button size='lg' variant='default'>
							Start Your Free Trial
						</Button>
					</Link>
				</motion.div>
			</div>
		</section>
	);
}
