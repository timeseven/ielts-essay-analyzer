'use client';

import Link from 'next/link';
import { Button } from '@/components/ui/button';
import { motion, useScroll, useTransform } from 'motion/react';
import { useRef } from 'react';

export default function Hero() {
	const ref = useRef(null);
	const { scrollYProgress } = useScroll({
		target: ref,
		offset: ['start start', 'end start'],
	});

	const y = useTransform(scrollYProgress, [0, 1], ['0%', '50%']);

	return (
		<section
			id='hero'
			ref={ref}
			className='relative flex h-screen w-full items-center justify-center overflow-hidden bg-gradient-to-br from-indigo-500 via-purple-500 to-pink-500'
		>
			<motion.div style={{ y }} className='relative z-10 container mx-auto px-4 md:px-6'>
				<div className='flex flex-col items-center space-y-4 text-center'>
					<motion.h1
						className='text-4xl font-bold tracking-tighter text-white sm:text-5xl md:text-6xl lg:text-7xl/none'
						initial={{ opacity: 0, y: 20 }}
						animate={{ opacity: 1, y: 0 }}
						transition={{ duration: 0.5 }}
					>
						AI-Powered IELTS Essay Analysis
					</motion.h1>
					<motion.p
						className='mx-auto max-w-[700px] text-xl text-gray-100 md:text-2xl'
						initial={{ opacity: 0, y: 20 }}
						animate={{ opacity: 1, y: 0 }}
						transition={{ duration: 0.5, delay: 0.2 }}
					>
						Unlock insights from your IELTS essays with our advanced AI analysis platform.
					</motion.p>
					<motion.div
						initial={{ opacity: 0, y: 20 }}
						animate={{ opacity: 1, y: 0 }}
						transition={{ duration: 0.5, delay: 0.4 }}
					>
						<Link href='/client'>
							<Button size='lg' className='mt-6 text-lg hover:scale-105'>
								Start Analyzing
							</Button>
						</Link>
					</motion.div>
				</div>
			</motion.div>
		</section>
	);
}
