"use client";

import {
  Navbar as NextUINavbar,
  NavbarContent,
  NavbarMenu,
  NavbarMenuToggle,
  NavbarBrand,
  NavbarItem,
  NavbarMenuItem,
} from "@heroui/navbar";
import { Link } from "@heroui/link";
import NextLink from "next/link";
import { usePathname } from "next/navigation";
import React from "react";

import { siteConfig } from "@/config/site";
import { ThemeSwitch } from "@/components/theme-switch";
import { GithubIcon } from "@/components/icons";

import MaisLogo from "./mais-logo";

export const Navbar = () => {
  const pathname = usePathname();

  return (
    <NextUINavbar
      isBordered
      classNames={{
        item: [
          "flex",
          "relative",
          "h-full",
          "items-center",
          "data-[active=true]:text-primary",
          "data-[active=true]:after:content-['']",
          "data-[active=true]:after:absolute",
          "data-[active=true]:after:bottom-0",
          "data-[active=true]:after:left-0",
          "data-[active=true]:after:right-0",
          "data-[active=true]:after:h-[2px]",
          "data-[active=true]:after:rounded-[2px]",
          "data-[active=true]:after:bg-primary",
        ],
      }}
      maxWidth="xl"
      position="sticky"
    >
      <NavbarContent>
        <NavbarMenuToggle className="sm:hidden" />
        <NavbarBrand>
          <NextLink className="" href="/">
            <div className="flex gap-2 items-center justify-content">
              <MaisLogo />
              <p className="font-bold text-inherit">MAIS</p>
            </div>
          </NextLink>
        </NavbarBrand>
      </NavbarContent>
      <NavbarContent className="hidden sm:flex gap-4" justify="center">
        {siteConfig.navItems.map((item) => (
          <NavbarItem key={item.href} isActive={pathname === item.href}>
            <NextLink
              color={pathname === item.href ? "primary" : "foreground"}
              href={item.href}
            >
              {item.label}
            </NextLink>
          </NavbarItem>
        ))}
      </NavbarContent>

      <NavbarContent className="" justify="center">
        <NavbarItem className="">
          <Link isExternal aria-label="Github" href={siteConfig.links.github}>
            <GithubIcon className="text-default-500" />
          </Link>
        </NavbarItem>
        <ThemeSwitch />
      </NavbarContent>

      <NavbarContent className="" justify="end">
        <NavbarItem className="">
          <Link isExternal aria-label="API" href={siteConfig.links.api}>
            API
          </Link>
        </NavbarItem>
      </NavbarContent>

      <NavbarMenu>
        {siteConfig.navMenuItems.map((item, index) => (
          <NavbarMenuItem
            key={`${item}-${index}`}
            isActive={pathname === item.href}
          >
            <Link
              color={pathname === item.href ? "primary" : "foreground"}
              href={item.href}
              size="lg"
            >
              {item.label}
            </Link>
          </NavbarMenuItem>
        ))}
      </NavbarMenu>
    </NextUINavbar>
  );
};
