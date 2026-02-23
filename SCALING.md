# Scaling Strategy: Handling 1 Million Scans Per Month

To handle 1 million scans per month (~33,000 scans per day, ~1,400 per hour), the following scaling strategy should be implemented:

## 1. Compute Scaling
- **Horizontal Scaling of Workers**: Spin up multiple Celery worker containers. Since each worker handles one crawl at a time, we need enough concurrency to handle the peak load.
- **Auto-scaling**: Use Kubernetes Horizontal Pod Autoscaler (HPA) to scale workers based on Redis queue depth.

## 2. Database Scaling
- **MongoDB Sharding**: Shard the `pages` and `scans` collections by `user_id` or `domain` to distribute the load across multiple servers.
- **Indexes**: Ensure proper indexing on `scan_id`, `user_id`, and `created_at` to keep query performance high.

## 3. Crawler Optimization
- **Proxy Rotation**: Use a proxy service (like Bright Data or Oxylabs) with Playwright to avoid IP bans when crawling at scale.
- **Headless Management**: Use **Browserless.io** or a similar service to manage headless browser instances at scale instead of running them inside the worker containers.

## 4. Caching & Performance
- **API Response Caching**: Use Redis to cache SEO results for a period (e.g., 24 hours) to prevent redundant crawls of the same domain.
- **CDN**: Serve the Next.js frontend and static assets via a CDN (Cloudflare/Vercel) to reduce server load.

## 5. Queue Management
- **Redis Cluster**: Deploy Redis in a cluster mode to handle high throughput of task messages.
- **Priority Queues**: Implement multiple queues (e.g., `high-priority` for paid users, `default` for free users) to ensure SaaS tier limits are respected.

## 6. Resource Limits
- Implement strict rate limiting at the Nginx or API level to prevent abuse.
- Set memory and CPU limits on Docker containers to prevent a single runaway process from taking down the host.
